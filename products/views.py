# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import get_language
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products with automatic language handling.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        """
        List products with language info in response.
        """
        response = super().list(request, *args, **kwargs)

        # Add language metadata
        response.data["meta"] = {
            "language": get_language(),
            "supported_languages": ["en", "fr"],
            "total_products": self.get_queryset().count(),
        }

        return response

    def retrieve(self, request, *args, **kwargs):
        """
        Get single product, ensuring translations exist.
        """
        instance = self.get_object()

        # Ensure translations exist for this product
        instance.ensure_translations()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def retranslate(self, request, pk=None):
        """
        Manually trigger re-translation of a product.
        Useful if translation quality needs improvement.
        """
        product = self.get_object()
        product.ensure_translations(force_refresh=True)

        return Response(
            {
                "status": "retranslation completed",
                "product_id": product.id,
                "language": get_language(),
            }
        )


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.ensure_translations()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
