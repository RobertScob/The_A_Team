from django.urls import path 
from market import views

app_name = 'market'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('item/<uuid:itemID>/', views.item, name='item'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('register/', views.register, name='register'),
    path("purchase/<uuid:itemID>/", views.purchase_item, name="purchase_item"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search_items/', views.search_items, name='search_items'),
]

