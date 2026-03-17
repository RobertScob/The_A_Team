from market import models
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'student_id', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('profile_photo_url',)


