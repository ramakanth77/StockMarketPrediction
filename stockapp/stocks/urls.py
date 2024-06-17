from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/<int:stock_id>/', views.stock_detail, name='stock_detail'),
    path('stock/<int:stock_id>/<str:period>/', views.stock_detail, name='stock_detail'),
]
