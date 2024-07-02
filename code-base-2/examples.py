### Exercise 108 ###
$ python3 manage.py shell
from ecommerce.inventory.models import Brand, Category

Brand.objects.all()
Brand.objects.all().values()

x = Brand.objects.all().query
print(x)
# returns SELECT "inventory_brand"."id", "inventory_brand"."name" FROM "inventory_brand"

### Exercise 109 ###
from ecommerce.inventory.models import Brand, Category
from django.db import connection

Brand.objects.all().query
connection.queries      # view all past queries performed

Brand.objects.all().filter(id=1)
connection.queries      # shows previous query and this new .filter() query

# Using SQL Cursor and SQL Query Format (returns QuerySet)
cursor = connection.cursor()
x = cursor.execute("SELECT * FROM inventory_brand")
for i in x:
    print(i)

# Using raw function (returns RawQuerySet)
x = Brand.objects.raw("SELECT * FROM inventory_brand")
for i in x:
    print(i)

### Exercise 110 ###
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# objects.get() will error out if there are two or more objects with '361' as its name
x = Brand.objects.get(name="361")       # does not return QuerySet
print(type(x))
print(x.name, x.id)
Brand.objects.all()

### Exercise 111 ###
x = Brand.object.get(id=100)     # Can use things like x.id cuz it's a QuerySet
x.id
x = Brand.object.raw("SELECT * FROM inventory_brand where id=1")
x.id                        # Error cuz can't do that with object.raw()

### Exercise 112 ###
Brand.objects.all()
Brand.objects.get(id=1)
Brand.objects.all().filter(id=1, name="361")            # .filter can return more than one (unlike .get)
Brand.objects.filter(id=1).filter(name="361")           # AND statement
Brand.objects.filter(id=1) | Brand.objects.filter(id=2) # OR statement
Brand.objects.all().filter(id__gt=10)                   # id Greater Than 10
Brand.objects.all().filter(id__lte=10)                  # id Less Than Equal to 10
Brand.objects.all().filter(name__startswith="a")        # name startswith 'a'
Brand.objects.all().exclude(id=1)                       # exclude id=1

### Exercise 113 ###
from ecommerce.inventory.models import Brand

x = Brand.objects.raw("SELECT * FROM inventory_brand WHERE id=1 AND name='361' OR id=2")
for i in x:
    print(i)

x = Brand.objects.raw("SELECT * FROM inventory_brand WHERE NOT id=1")
for i in x:
    print(i)

### Exercise 114 ###
from ecommerce.inventory.models import Brand, Product, ProductInventory, Media
from django.db import connection, reset_queries

ProductInventory.objects.all()
ProductInventory.objects.all().values()[0]

reset_queries()
connection.queries
ProductInventory.objects.filter(brand=1)            # same as .filter(brand_id=1) as seen in the database; brand is foreign key

# Find brand_id of brand name
x = ProductInventory.objects.filter()
x.values()
x[0].id
for i in x.values():
    print(i)
for i in x:
    print(i.id, i.brand_id)

# Foreign Key Lookup
# Search for brand name using foreign key association (ex: foreign_key__searchkey)
x = ProductInventory.objects.filter(brand_id__name="a.x.n.y.")
x.count()
for i in x.values():
    print(i)
for i in x:
    print(i.id, i.brand_id, i.sku, i.upc)

# "Reverse Foreign Key" (confusing as fuck. I think the idea is to find an entry (which contains id=8) in any other table that just so happens has a Brand Foreign Key that is found in the Brand table. In which that entry id returns back which 'brand_id' it is associated with.)
from ecommerce.inventory.models import Brand, Product, ProductInventory, Media
x = Brand.objects.filter(brand__id=8)       # returns "2 lips too" which is brand_id 8 but

# Filter based on category_id (easy stuff)
x = Product.objects.filter(category_id=4)

# Filter everything with a foreign key associated to category_id (using category_id__name) - which is the same as above
x = Product.objects.filter(category_id__name="sport and fitness")

# Now let's do "Reverse Foreign Key"
# According to Product Model, the related_name is 'category' (it is 'product' in the tutorial)
x = Category.objects.filter(category__name='widstar running sneakers')

# Return a product from ProductInventory based on a category name by chaining your way using foreign_key related_name id with foreign_key related_name id
x = ProductInventory.objects.filter(product_id__category_id__name="sport and fitness")
print(x.values())

# Another example
x = ProductInventory.objects.filter(product_id__category_id__id=8)
print(x.values())

### Exercise 115 - Exercise 117 (skip) ###

## Exercise 120 ###
from ecommerce.inventory.models import Brand, Product, ProductInventory, Media
Brand.objects.filter(id=1).update(name="newdata")
Brand.objects.filter(id__range=(1,5)).update(name="newdata")
Brand.objects.update_or_create(name="strykersoft")  # returns true if created, false if updated
# added nickname to models.py -> Brand then migrated
Brand.objects.update_or_create(name="veryacademy", nickname="new")   # returns true if created, false if updated

# Force 'update' cuz sometimes it will just create a new record instead of updating
Brand.objects.update_or_create(name="veryacademy", nickname="new", defaults={"nickname":"newnickname"})

### Exercise 122 (bulk update) ###
obj = [Brand.objects.get(id=1),Brand.objects.get(id=2)]
obj[0].name="something"
obj[1].name="somethingelse"
Brand.objects.bulk_update(obj, ["name"])

data = [(1,'a'), (2,'b')]
id_set = [id for id, name in data]      # prints [1, 2]
brand_to_update = Brand.objects.filter(id__in=id_set)     # bulk update with __in
>>> print(brand_to_update)              # <QuerySet [<Brand: something>, <Brand: somethingelse>]>

new_update = []
for brand in brand_to_update:
    brand.name = next(name for id, name in data if id == brand.id)
    new_update.append(brand)
    print(brand.name)       # a then b
print(new_update)           # [<Brand: a>, <Brand: b>]
print(new_update[0].id)     # 1

Brand.objects.bulk_update(new_update, ['name'])
# id 1 and id 2 have successfully updated in the database to be 'a' and 'b'

### Exercise 125 (Deleting) ###
from ecommerce.inventory.models import Brand
Brand.objects.filter(id=1).delete()     # (1, {'inventory.Brand': 1})
Brand.objects.all().delete()            # (22, {'inventory.Brand': 22})