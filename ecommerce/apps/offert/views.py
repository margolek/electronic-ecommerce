from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Category, Price, Product, Images
from ecommerce.apps.offert.offert import Offert
from django.template.defaulttags import register


def home(request):
    home = Offert()
    category_list, category_len, carousel_qty, category = home.get_category_list()
    sale_list, sale_len, images, percentage_sale, sale = home.get_sale_list()
    descendent_count = [des.get_descendant_count() for des in category]

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
        'descendent_count': dict(zip(category, descendent_count)),
    }
    return render(request, "offert/index.html", context)


def subcategory(request, slug):
    category = Category.objects.filter(parent_id__slug=slug)
    descendent_count = [des.get_descendant_count() for des in category]

    @register.filter
    def put_variable(d, key):
        return d[key]

    try:
        # Get one category to define ancestors
        category_anc = category.first()
        ancestors = [m for m in category_anc.get_ancestors(
            ascending=False, include_self=False)]
    except:
        raise Http404

    title = slug.capitalize()

    context = {
        'category': category,
        'title': title,
        'ancestors': ancestors,
        'descendent_count': dict(zip(category, descendent_count)),
    }
    return render(request, "offert/subcategory.html", context)


def get_category_products(request, slug):
    product = Offert(slug=slug)
    category, products, ancestors, images, percentage_pr = product.get_product_list()

    @register.filter
    def put_variable(d, key):
        return d[key]

    context = {
        'category': category,
        'products': products,
        'ancestors': ancestors,
        'images': images,
        'percentage_pr':  dict(zip(products, percentage_pr)),
    }

    return render(request, "offert/products.html", context)


def indyvidual_product(request, slug, slug_product):
    product = Offert(slug=slug, slug_product=slug_product)
    product, images, price, product_rate, product_features, ancestors = product.product_indyvidual()
    images_len = range(len(images))

    context = {
        'product': product,
        'images': images,
        'price': price,
        'product_rate': product_rate,
        'product_features': product_features,
        'ancestors': ancestors,
        'images_len': images_len,
    }

    return render(request, "offert/product_indyvidual.html", context)
