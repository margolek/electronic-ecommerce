from django.urls import path

from . import views

app_name = "offert"

urlpatterns = [
    path("", views.home, name="offert"),
    path("<slug:slug>/", views.subcategory, name="subcategory"),
    path("<slug:slug>/products/", views.get_category_products, name="products")
]
