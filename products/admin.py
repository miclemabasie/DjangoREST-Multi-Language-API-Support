# admin.py
from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ["name", "price", "sku"]
    # Modeltranslation will automatically show translation fields


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ["name", "slug"]
