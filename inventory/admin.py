"""
    Admin
"""

import nested_admin
from django.contrib import admin

from .models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductType,
    SeasonalEvent,
)


class ProductImageInline(nested_admin.NestedStackedInline):
    """
    ProductImageInline
    """
    model = ProductImage
    extra = 1


class ProductLineInLine(nested_admin.NestedStackedInline):
    """
    ProductLineInLine
    """

    model = ProductLine
    inlines = [ProductImageInline]
    extra = 1


class ProductAdmin(nested_admin.NestedModelAdmin):
    """
    ProductAdmin
    """

    inlines = [ProductLineInLine]
    list_display = ("name", "category", "stock_status", "is_active")

    list_filter = (
        "category",
        "stock_status",
        "is_active",
    )

    search_fields = ("name",)


class SeasonalEventAdmin(admin.ModelAdmin):
    """
    SeasonalEventAdmin
    """

    list_display = ("name", "start_date", "end_date")


class AttributeValueInline(admin.TabularInline):
    """
    AttributeValueInline
    """

    model = AttributeValue
    extra = 1


class AttributeAdmin(admin.ModelAdmin):
    """
    AttributeAdmin
    """

    inlines = [AttributeValueInline]


class ChildTypeInline(admin.TabularInline):
    """
    ChildTypeInline
    """

    model = ProductType
    fk_name = "parent"
    extra = 1  # How many extra sub-categories


class ParentTypeAdmin(admin.ModelAdmin):
    """
    ParentCategoryAdmin
    """

    inlines = [ChildTypeInline]


class ChildCategoryInline(admin.TabularInline):
    """
    ChildCategoryInline
    """

    model = Category
    fk_name = "parent"
    extra = 1  # How many extra sub-categories


class ParentCategoryAdmin(admin.ModelAdmin):
    """
    ParentCategoryAdmin
    """

    inlines = [ChildCategoryInline]
    list_display = (
        "name",
        "parent_name",
    )

    def parent_name(self, obj):
        """
        parent_name
        """
        return obj.parent.name if obj.parent else None


admin.site.register(ProductType, ParentTypeAdmin)
admin.site.register(Category, ParentCategoryAdmin)
admin.site.register(SeasonalEvent, SeasonalEventAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductLine)
admin.site.register(Attribute, AttributeAdmin)
