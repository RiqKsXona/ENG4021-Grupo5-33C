from django.test import TestCase

from .models import Usuario


class MensagemSucessoTest(TestCase):

    def setUp(self):
        usuario = Usuario(nome="Ana", email="ana@exemplo.com", curso="Engenharia", matricula="1234567", perfil="Aluno")
        usuario.set_senha("senha123")
        usuario.save()

        sessao = self.client.session
        sessao["email_usuario"] = usuario.email
        sessao.save()

    def test_mostra_mensagem_depois_de_reportar(self):
        resposta = self.client.post("/reportar-perdido/", {
            "titulo": "Garrafa azul",
            "categoria": "utensilios",
            "local": "Biblioteca",
            "data": "2026-11-20T10:00",
            "descricao": "Garrafa de metal azul",
        }, follow=True)

        self.assertContains(resposta, "Item perdido publicado com sucesso!")
