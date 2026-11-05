from django.test import TestCase

from .models import ItemAchado, ItemPerdido, Usuario


class EditarExcluirTest(TestCase):

    def setUp(self):
        self.dono = Usuario.objects.create(nome="Ana", email="ana@exemplo.com", senha="x", curso="Engenharia", matricula="1", perfil="aluno")
        self.outro = Usuario.objects.create(nome="Beto", email="beto@exemplo.com", senha="x", curso="Engenharia", matricula="2", perfil="aluno")
        self.perdido = ItemPerdido.objects.create(usuario=self.dono, titulo="Garrafa azul", categoria="utensilios", local="Biblioteca")
        self.achado = ItemAchado.objects.create(usuario=self.dono, nome_objeto="Fone branco", categoria="eletronicos", onde_encontrou="L110", onde_esta_agora="comigo")

    def entrar(self, usuario):
        sessao = self.client.session
        sessao["email_usuario"] = usuario.email
        sessao.save()

    def test_dono_edita_item_perdido(self):
        self.entrar(self.dono)
        self.client.post(f"/item-perdido/{self.perdido.id}/editar/", {
            "titulo": "Garrafa verde",
            "categoria": "utensilios",
            "local": "Pilotis",
        })

        self.perdido.refresh_from_db()
        self.assertEqual(self.perdido.titulo, "Garrafa verde")
        self.assertEqual(self.perdido.local, "Pilotis")

    def test_dono_edita_item_achado(self):
        self.entrar(self.dono)
        self.client.post(f"/item-achado/{self.achado.id}/editar/", {
            "nome_objeto": "Fone preto",
            "categoria": "eletronicos",
            "onde_encontrou": "L110",
            "onde_esta_agora": "prefeitura",
        })

        self.achado.refresh_from_db()
        self.assertEqual(self.achado.nome_objeto, "Fone preto")

    def test_dono_exclui_item(self):
        self.entrar(self.dono)
        self.client.post(f"/item-perdido/{self.perdido.id}/excluir/")
        self.client.post(f"/item-achado/{self.achado.id}/excluir/")

        self.assertFalse(ItemPerdido.objects.exists())
        self.assertFalse(ItemAchado.objects.exists())

    def test_outra_pessoa_nao_edita_nem_exclui(self):
        self.entrar(self.outro)
        editar = self.client.post(f"/item-perdido/{self.perdido.id}/editar/", {"titulo": "Hackeado", "categoria": "outros", "local": "x"})
        excluir = self.client.post(f"/item-achado/{self.achado.id}/excluir/")

        self.assertEqual(editar.status_code, 404)
        self.assertEqual(excluir.status_code, 404)
        self.perdido.refresh_from_db()
        self.assertEqual(self.perdido.titulo, "Garrafa azul")
        self.assertTrue(ItemAchado.objects.exists())
