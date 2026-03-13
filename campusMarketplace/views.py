from django.shortcuts import render
from django.http import HttpResponse

def shop(request):
     return HttpResponse("This is the main page.")

def newItem(request):
     return HttpResponse("This is the new item page.")

def account(request):
     return HttpResponse("This is the account page.")

