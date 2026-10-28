from django.contrib import admin
from .models import ItemAchado, ItemPerdido, Usuario

admin.site.register(ItemAchado)

class ItemAchadoAdmin(admin.ModelAdmin):
    list_display = ("nome_objeto", "categoria", "onde_encontrou", "data_encontro", "onde_esta_agora")
    list_filter = ("categoria", "onde_esta_agora", "data_encontro")
    search_fields = ("nome_objeto", "descricao", "onde_encontrou")
    date_hierarchy = "data_encontro"

admin.site.register(ItemPerdido)
admin.site.register(Usuario)
