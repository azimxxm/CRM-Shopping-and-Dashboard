from django.forms import *
from .models import *

class orderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            "customer":Select(attrs={
                'class':'form-control',
            }),
            "product":Select(attrs={
                'class':'form-control',
            }),
            "status":Select(attrs={
                'class':'form-control',
            }),
            "note":TextInput(attrs={
                'class':'form-control',
            }),
        }