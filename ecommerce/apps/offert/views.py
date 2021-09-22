from django.shortcuts import get_object_or_404, render
from .models import Category, Price, Product, Images
from ecommerce.apps.offert.offert import Offert
from django.template.defaulttags import register


def home(request):
    home = Offert()
    category_list, category_len, carousel_qty = home.get_category_list()
    print(category_list)
    print(category_len)

    @register.filter()
    def to_int(value):
        return int(value)

    context = {
        'price_day': home.price_day,
        'percentage': home.day_product_percentage(),
        'available_qty': home.available_quantity(),
        'category_list': category_list,
        'carousel_qty': range(carousel_qty),
        'category_len': category_len,
        'day_product': home.day_product,
        'day_product_image': home.day_product_image,
    }
    return render(request, "offert/index.html", context)
