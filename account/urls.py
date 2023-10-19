from . import views
from django.urls import path

urlpatterns = [
    path("kyc-registration/", views.kyc_registration, name="kyc-registration"),
    path("account/<int:pk>", views.account_view, name="account"),
    path("search-account/", views.search_account, name="search_account"),
]
