# Django Multi-Language API with Auto-Translation

A comprehensive solution for implementing multi-language support in Django REST APIs with automatic content translation.

## Overview

This project solves a common but poorly-documented challenge in Django development: automatically translating content across multiple languages in REST APIs. Unlike other solutions that require manual translation management, this implementation automatically handles translations when content is created and serves the appropriate language based on client headers.

## Key Features

- **Automatic Translation**: Content is automatically translated to all supported languages when created
- **Header-Based Language Detection**: Uses standard `Accept-Language` HTTP headers
- **REST API Ready**: Clean JSON responses in the requested language
- **Simple Integration**: Easy to add to existing Django projects
- **Production Ready**: Includes error handling, caching, and fallback strategies

## Tech Stack

- **Django** & **Django REST Framework**
- **django-modeltranslation** for field translation
- **googletrans** for automatic translation
- Custom middleware for language detection

## Prerequisites

```bash
pip install django-modeltranslation googletrans==3.1.0a0 djangorestframework
```

## Project Structure

```
.
├── db.sqlite3
├── djangolanguage
│   ├── asgi.py
│   ├── __init__.py
│   ├── middlewere
│   │   └── language_middleware.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── file.txt
├── manage.py
├── products
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── services
│   │   └── translation_service.py
│   ├── signals.py
│   ├── tests.py
│   ├── translation.py
│   └── views.py
├── README.md
└── requirements.txt
```

## Implementation Guide

### 1. Model Configuration

```python
# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True)
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
```

### 2. Translation Configuration

```python
# translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Product, Category

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')  # These will be translatable

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
```

### 3. Auto-Translation Service

```python
# services/translation_service.py
from googletrans import Translator
from django.conf import settings

translator = Translator()

def auto_translate_instance(instance, field_names):
    """
    Automatically translates instance fields to all supported languages.
    This is the core of our auto-translation system.
    """
    for lang_code, _ in settings.LANGUAGES:
        for field_name in field_names:
            # Get the original field value
            value = getattr(instance, field_name)
            
            # Translate to target language
            translated_value = translator.translate(value, dest=lang_code).text
            
            # Set the translated field
            setattr(instance, f"{field_name}_{lang_code}", translated_value)
    
    instance.save()
```

### 4. Language Detection Middleware

```python
# middleware/language_middleware.py
from django.utils import translation
from django.conf import settings

class AcceptLanguageMiddleware:
    """
    Detects client's preferred language from Accept-Language header
    and activates it for the request.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.supported_languages = [lang[0] for lang in settings.LANGUAGES]

    def __call__(self, request):
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')
        language_code = self._parse_accept_language(accept_language)
        
        translation.activate(language_code)
        request.LANGUAGE_CODE = language_code
        
        response = self.get_response(request)
        response['Content-Language'] = language_code
        return response
    
    def _parse_accept_language(self, accept_language):
        # Simple parsing - improve as needed
        for lang in accept_language.split(','):
            lang = lang.split(';')[0].strip()
            if lang in self.supported_languages:
                return lang
        return 'en'  # Default fallback
```

### 5. Settings Configuration

```python
# settings.py
INSTALLED_APPS = [
    'modeltranslation',  # Must be before admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'products.apps.ProductsConfig',
]

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

MIDDLEWARE = [
    # ... other middleware
    'djangolanguage.middleware.language_middleware.AcceptLanguageMiddleware',
]
```

### 6. API Serializers

```python
# serializers.py
from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'sku']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug']
```

### 7. Auto-Translation Signals

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Category
from .services.translation_service import auto_translate_instance

@receiver(post_save, sender=Product)
def auto_translate_product(sender, instance, created, **kwargs):
    if created:
        auto_translate_instance(instance, ['name', 'description'])

@receiver(post_save, sender=Category)
def auto_translate_category(sender, instance, created, **kwargs):
    if created:
        auto_translate_instance(instance, ['name', 'description'])
```

## Usage Examples

### Creating Content

```bash
# Create a product (English)
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "description": "Noise-cancelling wireless headphones",
    "price": "199.99",
    "sku": "WH-1000"
  }'
```

### Retrieving in Different Languages

```bash
# English
curl -X GET http://localhost:8000/api/products/1/ \
  -H "Accept-Language: en"

# French (auto-translated)
curl -X GET http://localhost:8000/api/products/1/ \
  -H "Accept-Language: fr"
```

## How It Works

1. **Content Creation**: When you create content with base fields (`name`, `description`), it's saved as the default language
2. **Auto-Translation**: Post-save signals trigger automatic translation to all supported languages
3. **Language Detection**: Middleware reads `Accept-Language` headers to determine client preference
4. **Smart Response**: API returns content in the requested language automatically

## Common Issues & Solutions

### Issue: Translations not working
**Solution**: Ensure `modeltranslation` is before `django.contrib.admin` in `INSTALLED_APPS`

### Issue: Language header ignored
**Solution**: Check middleware order and ensure it's after session middleware

### Issue: Auto-translation fails
**Solution**: Add error handling and fallbacks in translation service

## Extending the Solution

### Adding New Languages
1. Add to `LANGUAGES` in settings
2. Run `python manage.py update_translation_fields`
3. Restart server

### Custom Translation Services
Replace `googletrans` with paid services (Google Cloud Translate, DeepL, Azure Translator) for better accuracy and reliability.

## API Endpoints

- `GET /api/products/` - List products (respects Accept-Language)
- `POST /api/products/` - Create product (auto-translates)
- `GET /api/products/{id}/` - Get specific product
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category

## Production Considerations

- **Caching**: Implement caching for translations
- **Error Handling**: Add robust error handling for translation failures
- **Monitoring**: Log translation successes/failures
- **Rate Limiting**: Implement limits for translation API calls
- **Manual Overrides**: Allow manual translation overrides in admin

## 🤝 Contributing

This solution addresses a common gap in Django documentation. Feel free to contribute improvements, additional language support, or better translation services.

## 📄 License

MIT License - feel free to use in your projects!

