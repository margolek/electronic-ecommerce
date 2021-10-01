from .models import Product, Price, Images, Category
from django.shortcuts import get_object_or_404
import numpy as np


class Offert:

    def __init__(self, **kwargs):

        if kwargs:
            try:
                self.slug = kwargs['slug']
            except:
                self.slug = ''

        try:
            self.price_day = Price.objects.get(day_product=True)
            self.day_product = Product.objects.get(
                id=self.price_day.product_id)
            self.day_product_image = self.day_product.product_image.filter(
                default=True).get()
        except:
            self.price_day = []
            self.day_product = []
            self.day_product_image = []

    def day_product_percentage(self):
        try:
            percentage = round(((self.price_day.regular-self.price_day.day_product_price) /
                                self.price_day.regular)*100, 0)
        except:
            percentage = []
        return percentage

    def available_quantity(self):
        try:
            available_qty = round((self.day_product.quantity/100)*100, 0)
        except:
            available_qty = []
        return available_qty

    def get_category_list(self, batch_size=3, rows_in_carousel=2):
        category = Category.objects.filter(level=0).order_by('id')
        query = [category[n:n+batch_size]
                 for n in range(0, len(category), batch_size)]
        query_len = len(query)
        carousel_qty = int(np.ceil(query_len/rows_in_carousel))
        # Output format (query, query_length, expected_number of carousel)
        return (query, query_len, carousel_qty, category)

    def get_sale_list(self, batch_size=2, items_in_carousel=3):
        sale = Product.objects.filter(price__in_sale=True).all()
        images = Images.objects.filter(
            product_id__in=[i.id for i in sale]).filter(default=True)
        query = [sale[n:n+batch_size] for n in range(0, len(sale), batch_size)]
        # This line is problematic beceause create multiple queries (replace in future)
        count_percentage = [int(round(
            ((x.price.regular-x.price.in_sale_price)/x.price.regular)*100, 0)) for x in sale]
        # percentage_query = [count_percentage[n:n+batch_size]
        #                     for n in range(0, len(count_percentage), batch_size)]
        query_len = len(query)
        return (query, query_len, images, count_percentage, sale)

    def get_product_list(self):
        category = get_object_or_404(Category, slug=self.slug)
        products = Product.objects.filter(category=category.id)
        images = Images.objects.filter(
            product_id__in=[i.id for i in products]).filter(default=True)
        count_percentage = [int(round(
            ((x.price.regular-x.price.in_sale_price)/x.price.regular)*100, 0)) for x in products]
        ancestors = [m for m in category.get_ancestors(
            ascending=False, include_self=True)]
        return (category, products, ancestors, images, count_percentage)
