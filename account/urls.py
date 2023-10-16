from . import views
from django.urls import path

urlpatterns = [
    path("kyc-registration/", views.kyc_registration, name="kyc-registration"),
    path("account/", views.account_view, name="account"),
]
