from django.urls import path, include
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    # path("home/", views.home, name="home"),
    # path("home/", views.home, name="home"),
]
