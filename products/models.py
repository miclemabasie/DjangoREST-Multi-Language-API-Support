from django.db import models

# Create your models here.
# models.py
from django.db import models


class Product(models.Model):
    # ONLY base fields - modeltranslation will create name_en, name_fr, etc.
    name = models.CharField(max_length=200)
    description = models.TextField()

    # Non-translatable fields
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True)
    image_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    # Base fields only
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
