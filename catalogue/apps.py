from django.apps import AppConfig


class CatalogueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalogue'
    verbose_name = 'محصول'
    verbose_name_plural = 'محصولات'
