from django import forms
from django.forms import ModelForm, Widget
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Enter your email address"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter your password "
        self.fields["password2"].widget.attrs["placeholder"] = "confirm your password"
        self.fields["username"].widget.attrs["placeholder"] = "Enter your username"


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Enter your email address"
        self.fields["password"].widget.attrs["placeholder"] = "Enter your password "
