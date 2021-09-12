from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Feature,
    FeatureCategory,
    Images,
    Price,
    Product,
    ProductFeature,
    ProductRate,
)


class FeatureCategoryInline(admin.TabularInline):
    model = FeatureCategory


class ProductRateInline(admin.TabularInline):
    model = ProductRate


class ImagesInline(admin.TabularInline):
    model = Feature


class ImagesInline(admin.TabularInline):
    model = Images


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature


class PriceInline(admin.TabularInline):
    model = Price


@admin.register(Category)
class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 25
    exclude = ["slug"]


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    inlines = [FeatureCategoryInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ["slug"]
    inlines = [ImagesInline, PriceInline, ProductFeatureInline, ProductRateInline]
