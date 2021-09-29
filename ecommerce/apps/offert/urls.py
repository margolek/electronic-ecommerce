from django.urls import path

from . import views

app_name = "offert"

urlpatterns = [
    path("", views.home, name="offert"),
    path("<full_path>/", views.subcategory, name="subcategory")
]
