from django.test import TestCase

from .models import Usuario


class CadastroEmailTest(TestCase):

    def test_login_com_email_em_maiuscula(self):
        self.client.post("/cadastro/", {
            "nomeUsuario": "Ana",
            "emailUsuario": " Ana.Souza@PUC-Rio.br ",
            "senhaUsuario": "senha123",
            "confirmaSenhaUsuario": "senha123",
            "cursoUsuario": "Engenharia",
            "matriculaUsuario": "1234567",
            "perfilUsuario": "Aluno",
        })

        self.assertTrue(Usuario.objects.filter(email="ana.souza@puc-rio.br").exists())

        resposta = self.client.post("/login/", {"emailLogin": "Ana.Souza@PUC-Rio.br", "senhaLogin": "senha123"})
        self.assertRedirects(resposta, "/pagina-inicial/", fetch_redirect_response=False)
