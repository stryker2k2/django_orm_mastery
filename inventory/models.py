"""
    Database Models
"""

import uuid

from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    """
    Product Database Class
    """

    IN_STOCK = "IS"
    OUT_OF_STOCK = "OOS"
    BACKORDERED = "BO"

    STOCK_STATUS = {
        IN_STOCK: "In Stock",
        OUT_OF_STOCK: "Out of Stock",
        BACKORDERED: "Back Ordered",
    }

    pid = models.CharField(max_length=255)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True)
    is_digital = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    stock_status = models.CharField(
        max_length=3, choices=STOCK_STATUS, default=OUT_OF_STOCK
    )
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    seasonal_event = models.ForeignKey(
        "SeasonalEvent", on_delete=models.SET_NULL, null=True, blank=True
    )
    product_type = models.ManyToManyField("ProductType", related_name="product_type")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # Return self.name to caller function (ex: admin portal)
    def __str__(self):
        return str(self.name)


class ProductLine(models.Model):
    """
    ProductLine Database Model
    """

    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.UUIDField(default=uuid.uuid4)
    stock_qty = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField()
    weight = models.FloatField()
    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    attribute_values = models.ManyToManyField(
        "AttributeValue", related_name="attribute_values"
    )


class ProductImage(models.Model):
    """
    ProductImage Database Model
    """

    alternative_text = models.CharField(max_length=200)
    url = models.ImageField()
    order = models.IntegerField()
    product_line = models.ForeignKey("ProductLine", on_delete=models.CASCADE)


class Category(models.Model):
    """
    Category Database Model
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Category Name",
        help_text="Enter a category",
    )
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=False)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        """
        Meta Class is a Django Built-In Class to modify Parent Class Metadata
        """

        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # Return self.name to caller function (ex: admin portal)
    def __str__(self):
        return str(self.name)


class SeasonalEvent(models.Model):
    """
    Category Database Model
    """

    id = models.BigAutoField(primary_key=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class Attribute(models.Model):
    """
    Attribute Database Model
    """

    name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self):
        return str(self.name)


class AttributeValue(models.Model):
    """
    AttributeValue Database Model
    """

    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attribute.name}: {self.attribute_value}"


class ProductType(models.Model):
    """
    ProductType Database Model
    """

    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        """
        Meta Class is a Django Built-In Class to modify Parent Class Metadata
        """

        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"

    # Return self.name to caller function (ex: admin portal)
    def __str__(self):
        return str(self.name)


class ProductLine_AttributeValue(models.Model):
    """
    ProductLine <--> AttributeValue Link Table
    """

    attribute_value = models.ForeignKey("AttributeValue", on_delete=models.CASCADE)
    product_line = models.ForeignKey("ProductLine", on_delete=models.CASCADE)


class Product_ProductType(models.Model):
    """
    Product <--> ProductType Link Table
    """

    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    product_type = models.ForeignKey("ProductType", on_delete=models.CASCADE)


# class StockControl(models.Model):
#     """
#     ONE-TO-ONE EXAMPLE
#     """
#     stock_qty = models.IntegerField()
#     name = models.CharField(max_length=100)
#     stock_product = models.OneToOneField("Product", on_delete=models.CASCADE)
