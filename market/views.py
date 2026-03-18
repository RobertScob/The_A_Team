from urllib import request

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from market.forms import UserForm, UserProfileForm, ItemForm
from django.contrib import messages
from .models import Item, ITEM_CATEGORY_CHOICES

def shop(request):
    category = request.GET.get("category", "")

    items = Item.objects.filter(status="AVAILABLE")

    if category:
        items = items.filter(category=category)

    context = {
        "items": items,
        "category_choices": ITEM_CATEGORY_CHOICES,
        "selected_category": category,
    }

    return render(request, "market/shop.html", context)
     

def register(request):
     registered = False
     if request.method == 'POST':
          user_form = UserForm(request.POST) 
          

          if user_form.is_valid():

               user = user_form.save(commit=False) 

               user.set_password(user_form.cleaned_data['password']) 
               user.save()

               messages.success(request, 
                                'Registration successful. You can now log in.') 
               return redirect('market:login')

          else: 
               print(user_form.errors) 

     else:
          user_form = UserForm() 

     login_form = AuthenticationForm()

     return render(request, 'market/registration.html', {'user_form': user_form, 
                                                  'login_form': login_form, 
                                                  'registered': registered})


def user_login(request):

     if request.method == 'POST':
          form = AuthenticationForm(request, data=request.POST)

          if form.is_valid():
               login(request, form.get_user())
               return redirect('market:shop')

     else:
          form = AuthenticationForm() 

     user_form = UserForm()

     return render(request, 'market/registration.html', {'login_form':form,
                                                  'user_form': user_form,
                                                  'registered': False})

               


def logout(request):
     return HttpResponse("This is the logout page.")

def newItem(request):
     return HttpResponse("This is the new item page.")

def account(request):
     return HttpResponse("This is the user account page.")