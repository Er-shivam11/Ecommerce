# forms.py
from django import forms
from .models import Product,Order
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomerRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'age', 'profile_image']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'multiple': False}),
        }
        
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

