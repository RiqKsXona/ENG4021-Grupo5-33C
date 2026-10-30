from django.contrib import admin
from .models import ItemAchado, ItemPerdido, Usuario
 
 
@admin.register(ItemAchado)
class ItemAchadoAdmin(admin.ModelAdmin):
    list_display = ("nome_objeto", "categoria", "onde_encontrou", "data_encontro", "onde_esta_agora")
    list_filter = ("categoria", "onde_esta_agora", "data_encontro")
    search_fields = ("nome_objeto", "descricao", "onde_encontrou")
    date_hierarchy = "data_encontro"
 
 
@admin.register(ItemPerdido)
class ItemPerdidoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "local", "data", "tem_foto")
    list_display_links = ("titulo",)
    list_filter = ("categoria", "data")
    search_fields = ("titulo", "descricao", "local")
    date_hierarchy = "data"
    ordering = ("-id",)
    list_per_page = 20
 
    fieldsets = (
        ("Item", {"fields": ("titulo", "categoria", "foto")}),
        ("Onde e quando", {"fields": ("local", "data")}),
        ("Detalhes", {"fields": ("descricao",)}),
    )
 
    @admin.display(boolean=True, description="Tem foto?")
    def tem_foto(self, obj):
        return bool(obj.foto)
 
 
admin.site.register(Usuario)
