# stocks/forms.py
from django import forms

class StockForm(forms.Form):
    ticker = forms.CharField(label='Stock Ticker', max_length=10)
