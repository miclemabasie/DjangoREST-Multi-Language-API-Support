# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Product, Category
from .services.translation_service import auto_translate_instance


# @receiver(post_save, sender=Product)
# def auto_translate_product(sender, instance, created, **kwargs):
#     if created:
#         auto_translate_instance(instance)


# @receiver(post_save, sender=Category)
# def auto_translate_category(sender, instance, created, **kwargs):
#     if created:
#         auto_translate_instance(instance)


# # signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Product, Category
from .services.translation_service import auto_translate_instance


@receiver(post_save, sender=Product)
def auto_translate_product(sender, instance, created, **kwargs):
    if created:
        # Use transaction on_commit to ensure we have an ID
        transaction.on_commit(
            lambda: auto_translate_instance(instance, ["name", "description"])
        )


@receiver(post_save, sender=Category)
def auto_translate_category(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: auto_translate_instance(instance, ["name", "description"])
        )
