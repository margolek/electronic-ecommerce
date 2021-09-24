from django.shortcuts import get_object_or_404, render
from .models import Category, Price, Product, Images
from ecommerce.apps.offert.offert import Offert
from django.template.defaulttags import register


def home(request):
    home = Offert()
    category_list, category_len, carousel_qty = home.get_category_list()
    sale_list, sale_len, images, percentage_sale, sale = home.get_sale_list()

    @register.filter
    def get_position_upper(d, key):
        return d[2*key]

    @register.filter
    def get_position_bottom(d, key):
        if len(d) % 2 != 0 and d[2*key] == d[-1]:
            return
        return d[2*key+1]

    @register.filter
    def put_variable(d, key):
        return d[key]

    # This filter is not used (check if call query is faster than for loop)
    # @register.filter
    # def default_image_url(item, pk):
    #     return Images.objects.filter(product_id=pk).filter(default=True).get().image.url

    context = {
        'price_day': home.price_day,
        'percentage': home.day_product_percentage(),
        'available_qty': home.available_quantity(),
        'category_list': category_list,
        'carousel_qty': range(carousel_qty),
        'category_len': category_len,
        'day_product': home.day_product,
        'day_product_image': home.day_product_image,
        'sale_list': sale_list,
        'sale_len': sale_len,
        'sale_qty': range(sale_len),
        'images': images,
        'percentage_sale': dict(zip(sale, percentage_sale)),
    }
    return render(request, "offert/index.html", context)
