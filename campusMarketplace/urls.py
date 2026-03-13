from django.urls import path 
from campusMarketplace import views

app_name = 'campusMarketplace'

urlpatterns = [
    path('', views.shop, name='shop'),
    # path('/category/<slug:category_name_slug>/', views.category, name='category'),
    # path('/item/<slug:item_name_slug>/', views.item, name='item'),
    path('newItem/', views.new_item, name='new_item'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('account/', views.account, name='account'),
    ]

