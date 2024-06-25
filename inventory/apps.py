"""
Main Application for Inventory App
"""

from django.apps import AppConfig


class InventoryConfig(AppConfig):
    """
    InventoryConfig Database Class
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory"
