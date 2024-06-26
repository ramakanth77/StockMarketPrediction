from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Stock, Holding


class HoldingForm(forms.ModelForm):
    class Meta:
        model = Holding
        fields = ['stock', 'quantity']
        labels = {
            'stock': 'Stock Ticker',
            'quantity': 'Number of Shares'
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['ticker', 'name']
