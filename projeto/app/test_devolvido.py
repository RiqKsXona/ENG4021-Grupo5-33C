from django.test import TestCase

from .models import ItemPerdido, Usuario


class DevolvidoTest(TestCase):

    def setUp(self):
        self.dono = Usuario.objects.create(nome="Ana", email="ana@exemplo.com", senha="x", curso="Engenharia", matricula="1", perfil="aluno")
        self.outro = Usuario.objects.create(nome="Beto", email="beto@exemplo.com", senha="x", curso="Engenharia", matricula="2", perfil="aluno")
        self.item = ItemPerdido.objects.create(usuario=self.dono, titulo="Garrafa azul", categoria="utensilios", local="Biblioteca")

    def entrar(self, usuario):
        sessao = self.client.session
        sessao["email_usuario"] = usuario.email
        sessao.save()

    def test_dono_marca_como_devolvido(self):
        self.entrar(self.dono)
        self.client.post(f"/item-perdido/{self.item.id}/devolvido/")

        self.item.refresh_from_db()
        self.assertTrue(self.item.devolvido)

    def test_outra_pessoa_nao_consegue_marcar(self):
        self.entrar(self.outro)
        resposta = self.client.post(f"/item-perdido/{self.item.id}/devolvido/")

        self.assertEqual(resposta.status_code, 404)
        self.item.refresh_from_db()
        self.assertFalse(self.item.devolvido)

    def test_devolvido_some_da_pagina_inicial(self):
        self.item.devolvido = True
        self.item.save()

        resposta = self.client.get("/pagina-inicial/")

        self.assertNotIn(self.item, resposta.context["itens_perdidos"])
