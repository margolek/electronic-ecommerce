from .models import FeatureCategory, Product, Price, Images, Category, ProductRate, ProductFeature, Feature
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
                self.slug_product = kwargs['slug_product']
            except:
                self.slug_product = ''

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

    def get_category_list(self, batch_size=4, rows_in_carousel=2):
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

    def product_indyvidual(self):

        # Get all necessary models
        category = get_object_or_404(Category, slug=self.slug)
        product = get_object_or_404(
            Product, slug=self.slug_product)
        images = Images.objects.filter(product_id=product.id)

        product_rate = ProductRate.objects.filter(product_id=product.id)
        product_rate_len = dict(zip([i.pk for i in product_rate], [
            i for i in range(1, len(product_rate)+1)]))

        if len(product_rate) == 0:
            rate = 0
        else:
            rate = np.mean([i.value for i in product_rate])

        stars = 0
        empty_stars = 0
        half_star = False
        if rate < 0.25:
            stars = 0
            empty_stars = 5
        elif rate >= 0.25 and rate < 0.75:
            stars = 0
            half_star = True
            empty_stars = 4
        elif rate >= 0.75 and rate <= 1.25:
            stars = 1
            empty_stars = 4
        elif rate > 1.25 and rate < 1.75:
            stars = 1
            half_star = True
            empty_stars = 3
        elif rate >= 1.75 and rate <= 2.25:
            stars = 2
            empty_stars = 3
        elif rate > 2.25 and rate < 2.75:
            stars = 2
            half_star = True
            empty_stars = 2
        elif rate >= 2.75 and rate <= 3.25:
            stars = 3
            empty_stars = 2
        elif rate > 3.25 and rate < 3.75:
            stars = 3
            half_star = True
            empty_stars = 1
        elif rate >= 3.75 and rate <= 4.25:
            stars = 4
            empty_stars = 1
        elif rate > 4.25 and rate < 4.75:
            stars = 4
            half_star = True
            empty_stars = 0
        elif rate >= 4.75:
            stars = 5
            empty_stars = 0

        ancestors = [m for m in category.get_ancestors(
            ascending=False, include_self=True)]
        ancestors_id = [m.id for m in category.get_ancestors(
            ascending=False, include_self=True)]
        feature_category_id = [i.feature_id for i in FeatureCategory.objects.filter(
            category_id__in=ancestors_id)]
        features = Feature.objects.filter(id__in=feature_category_id)

        product_features_id_value = [
            (i.feature_id, i.value) for i in ProductFeature.objects.filter(product_id=product.id)]

        product_features = Feature.objects.filter(
            id__in=[i[0] for i in product_features_id_value])

        features_name = [i.name for i in product_features]
        features_value = [i[1] for i in product_features_id_value]

        feature_value_dict = dict(zip(features_name, features_value))
        feature_len = dict(zip(features_name, [
                           i for i in range(1, len(feature_value_dict)+1)]))

        return (product, images, product_rate, product_rate_len, product_features,
                ancestors, stars, half_star, empty_stars, feature_value_dict, feature_len)
