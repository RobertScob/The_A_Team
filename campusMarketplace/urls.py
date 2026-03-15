from django.urls import path 
from campusMarketplace import views

app_name = 'campusMarketplace'

urlpatterns = [
    path('', views.shop, name='shop'),
    # path('/category/<slug:category_name_slug>/', views.category, name='category'),
    # path('/item/<slug:item_name_slug>/', views.item, name='item'),
    path('new-item/', views.createListing, name='newItem'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
    ]

