from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from account.models import Account

from userAuth.models import User


# import forms
from .forms import UserRegistrationForm, LoginForm

# Create your views here.


def loginUser(
    request,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    if request.user.is_authenticated:
        messages.warning(request, f"{request.user}, you are already logged in.")
        return redirect("account")
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            print("--try block--")

        except User.DoesNotExist:
            messages.warning(request, "Check your email address or password")
            return redirect("loginUser")
        auth = authenticate(request, email=email, password=password)
        if auth is not None:
            login(request, auth)
            account = Account.objects.get(user=request.user)
            pk = account.account_number
            messages.success(request, f"welcome back {user}")
            return redirect("account", pk)
        else:
            messages.warning(request, "Please check your email address or password")
            return redirect("loginUser")

    return render(request, "userAuth/login.html")


def logoutUser(request) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    logout(request)
    # messages.success(request, "Logged out successfully")
    return redirect("index")


def register(
    request,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            print("1")
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                print("2")
                new_user = form.save()
                username = form.cleaned_data["username"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password1"]
                messages.success(
                    request, f"Hey, {username} you have created a new account. "
                )
                return redirect("loginUser")
            else:
                print("something is wrong at the else for form validation")

                messages.warning(request, "Check the form is not valid")
                return redirect("loginUser")

        else:
            form = UserRegistrationForm()
        context = {
            "form": form,
        }
        return render(request, "userAuth/register.html", context)
