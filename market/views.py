from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import datetime

from .models import Item, Transaction, ItemPhoto, ITEM_CATEGORY_CHOICES
from .forms import (
     UserRegistrationForm,
     LoginForm,
     ItemForm,
     ItemPhotoForm,
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
          "CATEGORY_CHOICES": ITEM_CATEGORY_CHOICES,
     }

     return render(request, "market/home.html", context)
     

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

               

@login_required
def logout(request):
     auth_logout(request)
     return redirect("market:login")

@login_required
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
               "listed_date": item.listed_at,
          },
     )
     
@login_required
def create_listing(request):
     if request.method == "GET":
          item_form = ItemForm()
          photo_form = ItemPhotoForm()

          return render(request, "market/create_listing.html", {
               "item_form": item_form,
               "photo_form": photo_form,
          })
     
     elif request.method == "POST":
          item_form = ItemForm(request.POST)
          photo_form = ItemPhotoForm(request.POST, request.FILES)

          if item_form.is_valid() and photo_form.is_valid():

               item = item_form.save(commit=False)
               item.seller = request.user
               item.save()

               images = request.FILES.getlist("images")

               first_image = True

               for image in images:
                    photo = ItemPhoto.objects.create(
                         item=item,
                         image=image
                    )

               if first_image:
                    item.thumbnail = photo.image
                    item.save()
                    first_image = False

               return redirect("market:shop")
     
     return render(request, "market/create_listing.html", {
               "item_form": item_form,
               "photo_form": photo_form,
          })

@login_required
def purchase_item(request, itemID):
     item = get_object_or_404(Item, pk=itemID)

     try:
          process_purchase(request.user, item)

          Transaction.objects.create(
               buyer=request.user,
               item=item,
               type="PURCHASE",
               amount=item.price,
          )

          messages.success(request, "Purchase successful!")

     except Exception as e:
          messages.error(request, str(e))

     return redirect("market:item", itemID=itemID)

@login_required
def account(request):
     profile_form = ProfileForm(instance=request.user)
     topup_form = TopUpForm()

     if request.method == "POST":

          # Profile update
          if "update_profile" in request.POST:
               profile_form = ProfileForm(
                    request.POST,
                    instance=request.user
               )

               if profile_form.is_valid():
                    profile_form.save()
                    messages.success(request, "Profile updated.")
                    return redirect("market:dashboard")

          # Top-up balance
          if "topup" in request.POST:
               topup_form = TopUpForm(request.POST)

               if topup_form.is_valid():
                    amount = topup_form.cleaned_data["amount"]

                    Transaction.objects.create(
                         buyer=request.user,
                         type="TOPUP",
                         amount=amount,
                    )

                    request.user.account_balance += amount
                    request.user.save(update_fields=["account_balance"])

                    messages.success(request, "Balance topped up.")
                    return redirect("market:dashboard")

     return render(
          request,
          "market/account.html",
          {
               "profile_form": profile_form,
               "topup_form": topup_form,
          },
     )

@login_required
def dashboard(request):
     listings = request.user.items_listed.all()
     purchases = request.user.transactions.filter(type="PURCHASE")
     sales = Transaction.objects.filter(
          item__seller=request.user,
          type="PURCHASE",
     )

     context = {
          "listings": listings,
          "purchases": purchases,
          "sales": sales,
          "balance": request.user.account_balance,
     }

     return render(request, "market/dashboard.html", context)

@login_required
def search_items(request):
     q = request.GET.get("q")

     items = Item.objects.filter(title__icontains=q)

     return render(
               request,
               "components/item_results.html",
               {"items": items}
          )