from django.test import TestCase

from .models import Usuario


class TrocarSenhaTest(TestCase):

    def setUp(self):
        self.usuario = Usuario(nome="Ana", email="ana@exemplo.com", curso="Engenharia", matricula="1234567", perfil="Aluno")
        self.usuario.set_senha("senha123")
        self.usuario.save()

        sessao = self.client.session
        sessao["email_usuario"] = self.usuario.email
        sessao.save()

    def trocar(self, atual, nova, confirma):
        return self.client.post("/perfil/senha/", {
            "senhaAtual": atual,
            "novaSenha": nova,
            "confirmaNovaSenha": confirma,
        })

    def test_troca_a_senha(self):
        resposta = self.trocar("senha123", "novasenha", "novasenha")

        self.assertContains(resposta, "Senha trocada com sucesso!")
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.verificar_senha("novasenha"))

    def test_senha_atual_errada(self):
        resposta = self.trocar("errada", "novasenha", "novasenha")

        self.assertContains(resposta, "A senha atual está errada.")
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.verificar_senha("senha123"))

    def test_confirmacao_diferente(self):
        resposta = self.trocar("senha123", "novasenha", "outracoisa")

        self.assertContains(resposta, "As senhas não coincidem.")

    def test_sem_login_vai_para_o_login(self):
        self.client.logout()
        resposta = self.client.get("/perfil/senha/")

        self.assertRedirects(resposta, "/login/", fetch_redirect_response=False)
