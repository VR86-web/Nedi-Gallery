from django.contrib import admin
from django.contrib.admin import ModelAdmin

from nediGalleryProject.product.models import Product, Collection, Category


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'picture', 'price', 'category', 'short_description', 'description', 'collection',
                    'created_at', 'updated_at',)


@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
    list_display = ('name', 'description', 'picture',)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name',)

