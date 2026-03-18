from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Item, Transaction
from .forms import (
     UserRegistrationForm,
     LoginForm,
     ItemForm,
     TopUpForm,
     ProfileForm,
)
from .services import process_purchase

def shop(request):
     query = request.GET.get("q", "")
     category = request.GET.get("category", "")

     items = Item.objects.filter(status="AVAILABLE")

     if query:
          items = items.filter(
               Q(title__icontains=query) |
               Q(description__icontains=query)
          )

     if category:
          items = items.filter(category=category)

     context = {
          "items": items.order_by("-listed_at"),
          "query": query,
          "category": category,
     }

     return render(request, "market/shop.html", context)
     

def register(request):
     if request.user.is_authenticated:
          return redirect("market:shop")

     if request.method == "POST":
          form = UserRegistrationForm(request.POST)

          if form.is_valid():
               form.save()
               messages.success(request, "Account created. Please login.")
               return redirect("market:login")
     else:
          form = UserRegistrationForm()

     return render(request, "market/register.html", {"form": form})


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