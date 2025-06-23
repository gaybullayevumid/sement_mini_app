from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "brand",
            "type",
            "quality",
            "weight",
            "image",
            "description",
            "origin",
            "cement_class",
            "price",
        ]
