# ORM

``` python
$ python3 manage.py shell
>>> from inventory.models import Brand
>>> 
>>> Brand.objects.create(brand_id=1,name='nike')
>>> x = Brand.objects.all().query
>>> 
>>> print(x)
# SELECT "inventory_brand"."brand_id", "inventory_brand"."name", "inventory_brand"."nickname" FROM "inventory_brand"
```