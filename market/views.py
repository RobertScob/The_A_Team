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

     if request.user.is_authenticated:
          return redirect("market:shop")

     form = LoginForm(request.POST or None)

     if request.method == "POST" and form.is_valid():
          email = form.cleaned_data["email"]
          password = form.cleaned_data["password"]

          user = authenticate(request, email=email, password=password)

          if user:
               login(request, user)
               return redirect("market:shop")
          else:
               messages.error(request, "Invalid login credentials")

     return render(request, "market/login.html", {"form": form})

               


def logout(request):
     auth_logout(request)
     return redirect("market:login")

def item(request, itemID):
     item = get_object_or_404(Item, pk=itemID)

     is_seller = (
          request.user.is_authenticated
          and request.user == item.seller
     )

     return render(
          request,
          "market/item.html",
          {
               "item": item,
               "is_seller": is_seller,
          },
     )

def account(request):
     return HttpResponse("This is the user account page.")