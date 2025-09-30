# serializers.py
from rest_framework import serializers
from django.utils.translation import get_language
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "sku",
            "image_url",
            "created_at",
        ]

    def create(self, validated_data):
        # Create the product - parler will handle language
        product = Product.objects.create(**validated_data)
        return product


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Category
        fields = ["id", "name", "description", "slug"]

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category
