"""Products app configuration."""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"
    verbose_name = "Products"

    def ready(self):
        """Import signal handlers when app is ready."""
        from . import signals 
