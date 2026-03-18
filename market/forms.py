from market import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Item

class UserForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'student_id', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('profile_photo_url',)

class ItemForm(forms.ModelForm):
    
    photos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    
    class Meta:
        model = Item
        fields = ["title", "description", "category", "price", "photos"]