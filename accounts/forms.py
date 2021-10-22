from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']