from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
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
