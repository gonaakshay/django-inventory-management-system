from django import forms
from .models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = '__all__'

        widgets = {
            'manufacture_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'expiry_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }