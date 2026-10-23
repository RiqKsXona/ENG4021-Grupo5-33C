from django import forms
from .models import ItemPerdido


class ItemPerdidoForm(forms.ModelForm):
    class Meta:
        model = ItemPerdido
        fields = ["titulo", "categoria", "local", "data", "descricao"]
        labels = {
            "titulo": "O que você perdeu?",
            "categoria": "Categoria",
            "local": "Onde perdeu?",
            "data": "Quando perdeu?",
            "descricao": "Descrição",
        }
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }