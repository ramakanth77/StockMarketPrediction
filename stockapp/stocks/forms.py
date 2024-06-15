from django import forms

class StockForm(forms.Form):
    ticker = forms.CharField(label='Stock Ticker', max_length=10)
    name = forms.CharField(label='My Name', max_length=50)
    period = forms.ChoiceField(
        label='Data Period',
        choices=[
            ('1d', '1 Day'),
            ('5d', '5 Days'),
            ('1mo', '1 Month'),
            ('3mo', '3 Months'),
            ('6mo', '6 Months'),
            ('1y', '1 Year')
        ]
    )
