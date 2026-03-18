from django.urls import path 
from market import views

app_name = 'market'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('item/<uuid:itemID>/', views.newItem, name='item_form'),
    path('listing/', views.newItem, name='newItem'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
]

