from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="loginUser")
def index(request):
    return render(request, "core/index.html")


@login_required(login_url="loginUser")
def contact(request):
    return render(request, "core/contact.html")
