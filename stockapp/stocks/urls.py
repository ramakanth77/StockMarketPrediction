from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock/<int:stock_id>/', views.stock_detail, name='stock_detail'),
    path('stock/<int:stock_id>/<str:period>/', views.stock_detail, name='stock_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('holdings/', views.holdings, name='holdings'),
    path('predict/<str:ticker>/', views.predict_stock, name='predict_stock'),
]
