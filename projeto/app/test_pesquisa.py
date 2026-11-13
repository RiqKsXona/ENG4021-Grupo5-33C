from django.test import TestCase

from .models import ItemAchado, ItemPerdido, Usuario


class PesquisaTest(TestCase):

    def setUp(self):
        usuario = Usuario.objects.create(nome="Ana", email="ana@exemplo.com", senha="x", curso="Engenharia", matricula="1", perfil="aluno")
        ItemPerdido.objects.create(usuario=usuario, titulo="Garrafa azul", categoria="utensilios", local="Biblioteca")
        ItemPerdido.objects.create(usuario=usuario, titulo="Casaco cinza", categoria="roupas", local="Pilotis")
        ItemAchado.objects.create(usuario=usuario, nome_objeto="Fone branco", categoria="eletronicos", onde_encontrou="L110", onde_esta_agora="comigo")
        ItemAchado.objects.create(usuario=usuario, nome_objeto="Estojo", categoria="material_estudo", onde_encontrou="RDC", onde_esta_agora="comigo")

    def test_pesquisa_itens_perdidos(self):
        resposta = self.client.get("/pagina-inicial/", {"busca_perdidos": "garrafa"})

        titulos = [item.titulo for item in resposta.context["itens_perdidos"]]
        self.assertEqual(titulos, ["Garrafa azul"])
        self.assertEqual(resposta.context["aba"], "perdidos")

    def test_pesquisa_itens_achados(self):
        resposta = self.client.get("/pagina-inicial/", {"busca_achados": "FONE"})

        nomes = [item.nome_objeto for item in resposta.context["itens_achados"]]
        self.assertEqual(nomes, ["Fone branco"])
        self.assertEqual(resposta.context["aba"], "achados")

    def test_sem_pesquisa_mostra_tudo(self):
        resposta = self.client.get("/pagina-inicial/")

        self.assertEqual(len(resposta.context["itens_perdidos"]), 2)
        self.assertEqual(len(resposta.context["itens_achados"]), 2)
