from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, "core/index.html")


@login_required(login_url="loginUser")
def contact(request):
    return render(request, "core/contact.html")


def home(request):
    return render(request, "core/home.html")
