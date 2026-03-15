from django.shortcuts import render
from django.http import HttpResponse

def shop(request):
     return HttpResponse("This is the main page.")

def register(request):
     return HttpResponse("This is the registration page.")

def login(request):
     return HttpResponse("This is the login page.")

def logout(request):
     return HttpResponse("This is the logout page.")

def newItem(request):
     return HttpResponse("This is the new item page.")

def account(request):
     return HttpResponse("This is the user account page.")