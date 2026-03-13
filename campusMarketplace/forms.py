from accounts import models
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = models.User
        fields = models.User.REQUIRED_FIELDS + (models.User.USERNAME_FIELD, 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('profile_photo_url')


