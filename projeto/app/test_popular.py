from django.core.management import call_command
from django.test import TestCase

from .models import ItemAchado, ItemPerdido, Usuario


class PopularBancoTest(TestCase):

    def test_cria_os_exemplos(self):
        call_command("popular_banco", stdout=None)

        self.assertEqual(ItemPerdido.objects.count(), 20)
        self.assertEqual(ItemAchado.objects.count(), 8)
        self.assertTrue(Usuario.objects.get(email="mariana.costa@example.com").verificar_senha("123456"))

    def test_rodar_duas_vezes_nao_duplica(self):
        call_command("popular_banco", stdout=None)
        call_command("popular_banco", stdout=None)

        self.assertEqual(ItemPerdido.objects.count(), 20)
        self.assertEqual(Usuario.objects.count(), 10)
