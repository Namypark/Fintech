from . import views
from django.urls import path

urlpatterns = [
    path("dashbboard/", views.dashboard, name="dashboard"),
]
