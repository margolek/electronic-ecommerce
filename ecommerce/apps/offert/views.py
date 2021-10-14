from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Category, Price, Product, Images
from ecommerce.apps.offert.offert import Offert
import numpy as np
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    home = Offert()
    category_list, category_len, carousel_qty, category = home.get_category_list()
    sale_list, sale_len, images, percentage_sale, sale = home.get_sale_list()
    descendent_count = [des.get_descendant_count() for des in category]

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
    items_per_page = 4
    page = request.GET.get('page', 1)

    paginator_pr = Paginator(products, items_per_page)
    paginator_im = Paginator(images, items_per_page)
    paginator_per = Paginator(percentage_pr, items_per_page)

    try:
        products = paginator_pr.page(page)
        images = paginator_im.page(page)
        percentage_pr = paginator_per.page(page)
    except PageNotAnInteger:
        products = paginator_pr.page(1)
        images = paginator_im.page(1)
        percentage_pr = paginator_per.page(1)
    except EmptyPage:
        products = paginator_pr.page(paginator_pr.num_pages)
        images = paginator_im.page(paginator_im.num_pages)
        percentage_pr = paginator_per.page(paginator_per.num_pages)

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
    (product, images, product_rate, product_rate_len, product_features,
     ancestors, stars, half_star, empty_stars, feature_value_dict,
     feature_len) = product.product_indyvidual()

    images_len = range(len(images))

    context = {
        'product': product,
        'images': images,
        'product_rate': product_rate,
        'product_rate_len': product_rate_len,
        'product_features': product_features,
        'ancestors': ancestors,
        'images_len': images_len,
        'stars': range(stars),
        'half_star': half_star,
        'empty_stars': range(empty_stars),
        'feature_value_dict': feature_value_dict,
        'feature_len': feature_len,
    }

    return render(request, "offert/product_indyvidual.html", context)
