from django.test import TestCase

from .models import Usuario


class EditarPerfilTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(nome="Ana", email="ana@exemplo.com", senha="x", curso="Engenharia", matricula="1234567", perfil="Aluno")

    def entrar(self):
        sessao = self.client.session
        sessao["email_usuario"] = self.usuario.email
        sessao.save()

    def test_formulario_vem_preenchido(self):
        self.entrar()
        resposta = self.client.get("/perfil/editar/")

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'value="Ana"')

    def test_salva_as_alteracoes(self):
        self.entrar()
        resposta = self.client.post("/perfil/editar/", {
            "nome": "Ana Souza",
            "curso": "Engenharia de Produção",
            "matricula": "7654321",
            "perfil": "Professor",
        })

        self.assertRedirects(resposta, "/perfil/", fetch_redirect_response=False)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, "Ana Souza")
        self.assertEqual(self.usuario.perfil, "Professor")

    def test_sem_login_vai_para_o_login(self):
        resposta = self.client.get("/perfil/editar/")

        self.assertRedirects(resposta, "/login/", fetch_redirect_response=False)
