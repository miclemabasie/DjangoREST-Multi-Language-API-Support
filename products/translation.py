# translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Product, Category


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
    )  # These will become name_en, name_fr, description_en, description_fr


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")
