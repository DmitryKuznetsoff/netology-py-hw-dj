from django.contrib import admin

from api.models import Product, Collection, ProductCollection, ProductOrderPosition, Order, Review


class ProductCollectionInline(admin.TabularInline):
    model = ProductCollection


class ProductOrderPositionInline(admin.TabularInline):
    model = ProductOrderPosition


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    inlines = [ProductCollectionInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductOrderPositionInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

