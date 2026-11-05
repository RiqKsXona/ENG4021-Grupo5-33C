import json
from unittest.mock import patch

from django.test import TestCase, override_settings

from .models import ItemAchado, ItemPerdido, Usuario
from .notificacoes import avisar_donos


@override_settings(BREVO_API_KEY="chave-de-teste", EMAIL_REMETENTE="elo@exemplo.com")
class AvisoPorEmailTest(TestCase):

    def setUp(self):
        self.dono = Usuario.objects.create(nome="Ana", email="ana@exemplo.com", senha="x", curso="Engenharia", matricula="1", perfil="aluno")
        self.quem_achou = Usuario.objects.create(nome="Beto", email="beto@exemplo.com", senha="x", curso="Engenharia", matricula="2", perfil="aluno")
        ItemPerdido.objects.create(usuario=self.dono, titulo="Garrafa azul", categoria="utensilios", local="Biblioteca")
        ItemPerdido.objects.create(usuario=self.dono, titulo="Fone de ouvido", categoria="eletronicos", local="RDC")

    # A chamada à API é simulada para o teste não mandar email de verdade
    @patch("app.notificacoes.urllib.request.urlopen")
    def test_avisa_quem_perdeu_item_da_mesma_categoria(self, urlopen):
        urlopen.return_value.__enter__.return_value.status = 201

        achado = ItemAchado.objects.create(usuario=self.quem_achou, nome_objeto="Garrafa térmica", categoria="utensilios", onde_encontrou="Pilotis", onde_esta_agora="comigo")

        self.assertEqual(avisar_donos(achado), 1)
        pedido = urlopen.call_args[0][0]
        corpo = json.loads(pedido.data)
        self.assertEqual(pedido.full_url, "https://api.brevo.com/v3/smtp/email")
        self.assertEqual(pedido.get_header("Api-key"), "chave-de-teste")
        self.assertEqual(corpo["to"][0]["email"], "ana@exemplo.com")
        self.assertIn("Garrafa térmica", corpo["subject"])

    @patch("app.notificacoes.urllib.request.urlopen")
    def test_nao_avisa_quem_achou_o_proprio_item(self, urlopen):
        achado = ItemAchado.objects.create(usuario=self.dono, nome_objeto="Garrafa térmica", categoria="utensilios", onde_encontrou="Pilotis", onde_esta_agora="comigo")

        self.assertEqual(avisar_donos(achado), 0)
        urlopen.assert_not_called()

    @patch("app.notificacoes.urllib.request.urlopen")
    def test_reportar_achado_pelo_site_manda_o_aviso(self, urlopen):
        urlopen.return_value.__enter__.return_value.status = 201
        sessao = self.client.session
        sessao["email_usuario"] = self.quem_achou.email
        sessao.save()

        resposta = self.client.post("/reportar-achado/", {
            "nome_objeto": "Fone branco",
            "categoria": "eletronicos",
            "onde_encontrou": "L110",
            "onde_esta_agora": "comigo",
        })

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(urlopen.call_count, 1)

    @override_settings(BREVO_API_KEY="")
    @patch("app.notificacoes.urllib.request.urlopen")
    def test_sem_chave_nao_chama_a_api(self, urlopen):
        achado = ItemAchado.objects.create(usuario=self.quem_achou, nome_objeto="Garrafa térmica", categoria="utensilios", onde_encontrou="Pilotis", onde_esta_agora="comigo")

        self.assertEqual(avisar_donos(achado), 0)
        urlopen.assert_not_called()
