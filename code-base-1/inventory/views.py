from django.http import HttpResponse
from .models import Brand, Product, ProductInventory, ProductType, Stock
from django.db import IntegrityError, transaction


def new(request):
    try:
        with transaction.atomic():
            ProductInventory.objects.create(sku='123', upc='123', product_type_id=2, product_id=9,
                                            brand_id=1, retail_price='10.00', store_price='10.00',
                                            sale_price='10.00', weight='100')

            Stock.objects.create(product_inventory_id=1, units=100)
    except IntegrityError:
        return HttpResponse("Error")

    return HttpResponse("Hi")