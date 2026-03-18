from django import forms
from django.contrib.auth import get_user_model
from .models import Item, ItemPhoto

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "student_id",
        ]
    
    def clean(self):
        cleaned = super().clean()

        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")

        return cleaned
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user
    

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "title",
            "description",
            "category",
            "price",
        ]
        

class ItemPhotoForm(forms.Form):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False
    )
        

class TopUpForm(forms.Form):
    amount = forms.DecimalField(min_value=1)
    
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "profile_picture",
        ]