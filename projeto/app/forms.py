from django import forms
from .models import ItemPerdido, ItemAchado

class ItemPerdidoForm(forms.ModelForm):

    class Meta:
        model = ItemPerdido

        fields = [
            "foto",
            "titulo",
            "categoria",
            "local",
            "data",
            "descricao"
        ]

        labels = {
            "titulo": "O que você perdeu?",
            "categoria": "Categoria",
            "local": "Onde perdeu?",
            "data": "Quando perdeu?",
            "descricao": "Descrição",
        }

        widgets = {
            "foto": forms.FileInput(attrs={
                "accept": "image/*"
            }),
            "data": forms.DateInput(attrs={
                "type": "date"
            }),
            "descricao": forms.Textarea(attrs={
                "rows": 4
            }),
        }


class ItemAchadoForm(forms.ModelForm):

    class Meta:
        model = ItemAchado

        fields = [
            "foto",
            "nome_objeto",
            "categoria",
            "onde_encontrou",
            "data_encontro",
            "descricao",
            "onde_esta_agora",
        ]

        widgets = {
            "foto": forms.FileInput(attrs={
                "id": "foto",
                "accept": "image/*",
                "hidden": True
            }),

            "nome_objeto": forms.TextInput(attrs={
                "placeholder": "Ex: garrafa térmica amarela"
            }),

            "categoria": forms.Select(),

            "onde_encontrou": forms.TextInput(attrs={
                "placeholder": "Ex: L110, sala 204"
            }),

            "data_encontro": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),

            "descricao": forms.Textarea(attrs={
                "placeholder": "Detalhes sobre o objeto achado",
                "rows": 4
            }),

            "onde_esta_agora": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["categoria"].choices = [
            ("", "Selecione uma categoria")
        ] + list(ItemAchado.CATEGORIA_CHOICES)

        self.fields["onde_esta_agora"].choices = [
            ("", "Selecione uma localização")
        ] + list(ItemAchado.ONDE_ESTA_CHOICES)
