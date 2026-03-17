
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from market.forms import UserForm, UserProfileForm
from django.contrib import messages

def shop(request):
     return HttpResponse("This is the main page.")

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
               return redirect('campusMarketplace:login')

          else: 
               print(user_form.errors) 

     else:
          user_form = UserForm() 

     login_form = AuthenticationForm()

     return render(request, 'campusMarketplace/registration.html', {'user_form': user_form, 
                                                  'login_form': login_form, 
                                                  'registered': registered})


def user_login(request):

     if request.method == 'POST':
          form = AuthenticationForm(request, data=request.POST)

          if form.is_valid():
               login(request, form.get_user())
               return redirect('campusMarketplace:shop')

     else:
          form = AuthenticationForm() 

     user_form = UserForm()

     return render(request, 'campusMarketplace/registration.html', {'login_form':form,
                                                  'user_form': user_form,
                                                  'registered': False})

               


def logout(request):
     return HttpResponse("This is the logout page.")

def newItem(request):
     return HttpResponse("This is the new item page.")

def account(request):
     return HttpResponse("This is the user account page.")