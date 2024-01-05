# forms.py
from django import forms
from .models import Product,Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Optionally, you can customize widget attributes or add placeholders here
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 5, 'cols': 40})

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['categories', 'products', 'carts']

