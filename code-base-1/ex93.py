# Example 93 and beyond
# These are the commands entered into `python3 manage.py shell`

from inventory.models import Brand
Brand.objects.all()
Brand.objects.all().delete()
Brand.objects.create(brand_id=1, name='nike')

# Example 94
from inventory.models import Brand
Brand.objects.all()
Brand.objects.all().delete()

# Using .save() instead of object.create()
Brand(brand_id=100,name='nike').save()

# Or...
x = Brand(brand_id=100,name='nike')
x.save()

# Or...
x = Brand(brand_id=100,name='nike')
x.brand_id=1000
x.name='nike1000'
x.nickname='myshoe'
x.save()

# Another .save() example
from inventory.models import Brand, Category
x = Category(name='trainers', slug='trainers', is_active=True)
x.save()
Category.objects.all().values()

# Exercise 95 (save vs create)
from inventory.models import Brand, Category

# Using Brand as example since we have to define the Primary Key
Brand.objects.all().delete()
Brand.objects.create(brand_id=1,name='nike')    # doing this twice causes "UNIQUE" IntegrityError
Brand(brand_id=1,name='nike').save()            # doing this twice WILL NOT ERROR (cuz it's overwritting)
Brand.objects.all().values()
Brand(brand_id=1,name='rebook').save()
Brand.objects.all().values()

# Using Category as example since Django auto-defines the Primary Key
# id increments; even if previous rows have been deleted
Category.objects.all().delete()
Category.objects.create(name='trainers', slug='trainers', is_active=True)   # doing twice fails cuz slug = UNIQUE
Category.objects.create(pk=3, name='trainers', slug='trainers', is_active=True)  # can use 'ok' to access variable declared as primary_key; will also fail
Category.objects.create(id=3, name='trainers', slug='trainers', is_active=True)  # same as before but using 'id=3'

# This will save with no errors
x = Category(pk=3, name='trainers', slug='trainers', is_active=True)
x.save()
Category.objects.all().values()

# modifies pk3's name & slug without issue
x = Category(pk=3, name='trainers100', slug='trainers100', is_active=True)
x.save()
Category.objects.all().values()

# Do SQL Queries directly (using create)
from django.db import connection, reset_queries
Brand.objects.all().delete()
Category.objects.all().delete()
reset_queries()
Brand.objects.create(brand_id=1,name='nike')
connection.queries  # returns... 'INSERT INTO "inventory_brand"

# Same (using save)
reset_queries()
Brand(brand_id=1000,name='nike1000').save()
connection.queries  # returns... 'UPDATE "inventory_brand" then 'INSERT INTO "inventory_brand" when brand_id 1000 not found
reset_queries()
Brand(brand_id=1000,name='nike1000').save()
connection.queries   # only does... 'UPDATE "inventory_brand" cuz brand_id 1000 already exists

# Example 96 (Building SQL Queries and Executing)
from django.db import connection
from inventory.models import Brand

Brand.objects.all().delete()
Category.objects.all().delete()

statement = "INSERT INTO inventory_brand (brand_id, name, nickname) VALUES (%s, %s, %s)"
args = ['1','nike', '']

cursor = connection.cursor()
cursor.execute(statement, args)

# View (in SQL) how Django does it
reset_queries()
Brand.objects.all().delete()
Brand.objects.create(brand_id=1,name='nike')
Brand.objects.all().values()
connection.queries

# Example 97 (Connecting Foreign Keys to Primary Keys)
from inventory.models import Product, ProductInventory, ProductType, Brand

# Create a Brand (with brand_id)
Brand.objects.create(brand_id=1, name='nike')
Brand.objects.all().values()

# Create a Product (with auto-populated id)
Product.objects.all().delete()
Product(web_id='1234', slug='nike-shoe-1', name='nike-shoe-1', description='ex2', is_active=True).save()
Product.objects.all().values()

# Create a ProductType (with auto-populated id)
ProductType.objects.create(name='shoe')
ProductType.objects.all().values()

# Create a Product Inventory Item (with sku) that connects to Product, ProductType, and Brand via Foreign Keys
# You do that by calling the foreign key + the keyword "_id" (ex: product_type fk is product_type_id)
# View each Model Table to verify the right keys ( <Model>.objects.all().values() )
ProductInventory.objects.create(sku='123', upc='123', product_type_id=1, product_id=1, brand_id=1,
                                retail_price='10.00', store_price='10.00', sale_price='10.00', weight='100')

# Testing out the "Deleting" of items (and if they are protected, cascaded, null, etc)
Product.objects.all().delete()              # Error - protected foreign keys

# MASS DELETE
Brand.objects.all().delete()
Product.objects.all().delete()
ProductInventory.objects.all().delete()
ProductType.objects.all().delete()
reset_queries

# Exercise 98 (DateTime)
Brand.objects.create(brand_id=1, name='nike')
Product(web_id='1234', slug='nike-shoe-1', name='nike-shoe-1', description='ex2',is_active=True).save()
ProductType.objects.create(name='shoe')

Brand.objects.all().values()
Product.objects.all().values()
ProductType.objects.all().values()

from django.db import connection

cursor = connection.cursor()
cursor.execute("INSERT INTO inventory_productinventory(sku,upc,product_type_id,product_id, brand_id, is_active, is_default, retail_price, store_price, sale_price, is_on_sale, is_digital, weight, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",['123','123', 2, 2, 1, True, True, '10.00', '10.00', '10.00', True, True, '100', '2024-06-26 20:58:30.485810', '2024-06-26 20:58:30.485810'])

# Now that we have populated product inventory table, we see that created_at and modifed_at are blank (sqlite extension to view table)
import datetime
datetime_object = datetime.datetime.now()
print(datetime_object)

# We deleted the database... and repopulating it now with a fully filled cursor.execute string because django required that all fields had some sort of data
from inventory.models import Product, ProductInventory, ProductType, Brand

Brand.objects.create(brand_id=1, name='nike')
Product(web_id='1234', slug='nike-shoe-1', name='nike-shoe-1', description='ex2',is_active=True).save()
ProductType.objects.create(name='shoe')

Brand.objects.all().values()
Product.objects.all().values()
ProductType.objects.all().values()

from django.db import connection

cursor = connection.cursor()
cursor.execute("INSERT INTO inventory_productinventory(sku,upc,product_type_id,product_id, brand_id, is_active, is_default, retail_price, store_price, sale_price, is_on_sale, is_digital, weight, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",['123','123', 1, 1, 1, True, True, '10.00', '10.00', '10.00', True, True, '100', '2024-06-26 20:58:30.485810', '2024-06-26 20:58:30.485810'])
ProductInventory.objects.all().values()

# Exercise 99 (Many-to-Many)
# Product class has a many-to-many category called "Category"
# We can find this in the sqlite database as "inventory_product_category"
# It only have two fields (product_id & category_id) to connect the two
from inventory.models import Product, ProductInventory, ProductType, Brand, Category
from django.db import connection, reset_queries

Brand.objects.all().delete()
Product.objects.all().delete()
ProductInventory.objects.all().delete()
ProductType.objects.all().delete()
Category.objects.all().delete()
reset_queries

x = Product(web_id='12345', slug='ex1', name='ex1', description='ex1', is_active=True)
x.save()
y = Category(name='Flip-Flops', slug='flip-flops', is_active=True)
y.save()
Product.objects.all().values()
Category.objects.all().values()

# Associate a new product to a category
x = Product(web_id='123456', slug='ex10', name='ex10', description='ex10', is_active=True)
x.save()

x = Product.objects.get(id=4)
y = Category.objects.get(id=1)
x.category.add(y)       # Associate with 'Flip-Flop' Category (in inventory_product_category table)

# Make multiple categories (to associate product with multiples)
y = Category(name='Flip-Flops2', slug='flip-flops2', is_active=True)
y.save()

y = Category.objects.all()

x = Product(web_id='1234567', slug='ex100', name='ex100', description='ex100', is_active=True)
x.save()

x.category.add(*y)      # prod_id 5 is now associate to cat_id 1 & cat_id 2 in inv_prod_cat table

# Exercise 100
from inventory.models import Product, ProductInventory, ProductType, Brand, Category
from django.db import connection, reset_queries

Brand.objects.all().delete()
Product.objects.all().delete()
ProductInventory.objects.all().delete()
ProductType.objects.all().delete()
Category.objects.all().delete()
reset_queries()

x = Product(web_id='1234', slug='ex1', name='ex1', description='ex1', is_active=True)
x.save()

y = Category(name='Flip-Flops', slug='flip-flops', is_active=True)
y.save()

connection.queries
reset_queries()

x.category.add(y)

connection.queries         # see "INSERT OR IGNORE INTO <table> pid, cid SELECT 6,3"
reset_queries()

cursor = connection.cursor()
cursor.execute("INSERT INTO inventory_product (web_id,slug,name,description,is_active,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)", ['123456', 'ex4', 'ex4', 'ex4', True, '2024-06-26 20:58:30.485810', '2024-06-26 20:58:30.485810'])
cursor.execute("INSERT INTO inventory_category (name, slug, is_active, lft, rght, tree_id, level) VALUES (%s,%s,%s,%s,%s,%s,%s)", ['Flip-Flop', 'flipflops', True, 1,2,1,0])
Product.objects.all().values()
Category.objects.all().values()

# Using SQL Query instead of doing x.category.add(y)
cursor.execute("INSERT INTO inventory_product_category (product_id, category_id) VALUES (%s, %s)", [7,4])

# Exercise 101
from inventory.models import Product, ProductInventory, ProductType, Brand, Category
from django.db import connection, reset_queries

Brand.objects.all().delete()
Product.objects.all().delete()
ProductInventory.objects.all().delete()
ProductType.objects.all().delete()
Category.objects.all().delete()
reset_queries()

Product.objects.create(web_id='1234', slug='ex1', name='ex1', description='ex1', is_active=True)
Brand.objects.create(brand_id=1, name='nike')
ProductType.objects.create(name='shoe')

# use atomic() to make sure that both commits either both happen... or return error (in views.py)
try: with transaction.atomic(): except IntegrityError

# Exercise 102 (one-to-one relationship)
# Erase SQL Database & re-migrate & re-populate
from inventory.models import Product, ProductInventory, ProductType, Brand, Category, Stock
from django.db import connection, reset_queries

Product.objects.create(web_id='1234', slug='ex1', name='ex1', description='ex1', is_active=True)
Brand.objects.create(brand_id=1, name='nike')
ProductType.objects.create(name='shoe')
ProductInventory.objects.create(sku='123', upc='123', product_type_id=1, product_id=1, brand_id=1,
                                retail_price='10.00', store_price='10.00', sale_price='10.00', weight='100')
Stock.objects.create(product_inventory_id=1, units=100)

# Exercise 103 (insert multiple objects into one table)
from inventory.models import Brand
Brand.objects.bulk_create(
    [Brand(brand_id='1', name='1'),
     Brand(brand_id='2', name='2')]
)

data = [{'brand_id':3, 'name':'3'},
        {'brand_id':4, 'name':'4'}]

Brand.objects.bulk_create([Brand(**ab) for ab in data])

# Exercise 105 (fixtures)
from inventory.models import Product, ProductInventory, ProductType, Brand, Category
from django.db import connection, reset_queries

Brand.objects.all().delete()
Product.objects.all().delete()
ProductInventory.objects.all().delete()
ProductType.objects.all().delete()
Category.objects.all().delete()
Stock.objects.all().delete()
reset_queries()

$ python3 manage.py loaddata inventory_brand
# > Installed 2 object(s) from 1 fixture(s)


