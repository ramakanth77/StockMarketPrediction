from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    current_price_inr = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker

class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.FloatField(default=0.0)
    purchase_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stock.ticker} - {self.quantity} shares"

class StockHistory(models.Model):
    stock = models.ForeignKey(Stock, related_name='history', on_delete=models.CASCADE)
    time = models.DateTimeField()
    price = models.FloatField()
