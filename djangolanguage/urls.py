from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, CategoryViewSet


router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [path("api/", include(router.urls)), path("admin/", admin.site.urls)]
