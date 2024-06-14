# stocks/urls.py
from django.urls import path
from .views import stock_view

urlpatterns = [
    path('', stock_view, name='stock_view'),
]


