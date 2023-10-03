from django.urls import path, include
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("sign-in/", views.loginUser, name="loginUser"),
    path("sign-out/", views.logoutUser, name="logoutUser"),
]
