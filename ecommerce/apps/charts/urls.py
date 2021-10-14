from django.urls import path

from . import views

app_name = "charts"

urlpatterns = [
    path("", views.home, name="dashboard"),
]
