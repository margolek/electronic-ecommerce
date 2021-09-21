from django.shortcuts import get_object_or_404, render
from .models import Category, Price, Product, Images
from ecommerce.apps.offert.offert import Offert


def home(request):
    category_list = list(
        enumerate(Category.objects.filter(level=0).order_by('id'), start=1))
    home = Offert()
    context = {
        'price_day': home.price_day,
        'percentage': home.day_product_percentage(),
        'available_qty': home.available_quantity(),
        'category_list': category_list,
        'day_product': home.day_product,
        'day_product_image': home.day_product_image,
    }
    return render(request, "offert/index.html", context)
