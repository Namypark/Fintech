from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, "core/index.html")


def home(request):
    return render(request, "core/home.html")
