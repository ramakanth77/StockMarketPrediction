from django.contrib.auth.models import User
from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    current_price_inr = models.FloatField(null=True, blank=True)
    percent_change = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker

class StockHistory(models.Model):
    stock = models.ForeignKey(Stock, related_name='history', on_delete=models.CASCADE)
    time = models.DateTimeField()
    price = models.FloatField()

class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def current_value(self):
        return self.quantity * self.stock.current_price_inr

    def __str__(self):
        return f'{self.user.username} holds {self.quantity} of {self.stock.ticker}'
