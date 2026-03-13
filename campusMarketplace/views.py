from django.shortcuts import render
from django.http import HttpResponse

def shop(request):
     return HttpResponse("This is the main page.")

def newItem(request):
     return HttpResponse("This is the new item page.")

def register(request):
     return HttpResponse("This is the registration page.");

def user_login(request):
     return HttpResponse("This is the login page.")

def user_logout(request):
     return HttpResponse("This is the logout page.")

def account(request):
     return HttpResponse("This is the account page.")