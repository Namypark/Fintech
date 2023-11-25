from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "core/index.html")


def home(request):
    return render(request, "core/home.html")


def error_404(request, exception):
    print(exception)
    return render(request, "core/error404.html", status=404)
