from django.urls import path 
from rango import views

app_name = 'campusMarketplace'

urlpatterns = [
    path('', views.shop, name='shop'),
    
    ]

