from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fetch_stock', views.fetch_stock, name='fetch_stock')
]