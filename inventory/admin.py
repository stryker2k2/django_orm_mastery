"""
    Admin
"""
from django.contrib import admin
from .models import Category, Product


# class CategoryAdmin(admin.ModelAdmin):
#     """
#         Category Admin
#     """
#     prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category)
admin.site.register(Product)
