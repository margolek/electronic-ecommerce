from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category, Feature, Images, Price, Product

admin.site.register(Feature)


class ImagesInline(admin.TabularInline):
    model = Images


class PriceInline(admin.TabularInline):
    model = Price


@admin.register(Category)
class CustomMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 25
    exclude = ["slug"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ["slug"]
    inlines = [ImagesInline, PriceInline]
