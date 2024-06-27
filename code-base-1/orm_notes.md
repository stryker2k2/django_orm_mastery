# ORM
All python shell examples are done with\
`$ python3 manage.py shell`

### Query Database
``` python
>>> from inventory.models import Brand
>>> 
>>> Brand.objects.create(brand_id=1,name='nike')
>>> x = Brand.objects.all().query
>>> 
>>> print(x)
# SELECT "inventory_brand"."brand_id", "inventory_brand"."name", "inventory_brand"."nickname" FROM "inventory_brand"
```

### Reset Database
``` python
>>> from inventory.models import Brand
>>> Brand.objects.all()
>>> Brand.objects.all().delete()
>>> Brand.objects.create(brand_id=1,name='nike')
>>> 
>>> from django.db import connection, reset_queries
>>> connection.queries
# [{'sql': 'SELECT "inventory_brand"."brand_id", "inventory_brand"."name"...}]
>>> reset_queries()
>>> connection.queries
# []
>>> Brand.objects.all()
>>> connection.queries
# [{'sql': 'SELECT "inventory_brand"."brand_id", "inventory_brand"."name", "inventory_brand"."nickname" FROM "inventory_brand" LIMIT 21', 'time': '0.000'}]
```

### SQL PrettyPrint
```python
$ pip install pygments sqlparse
>>> from pygments import highlight
>>> from pygments.formatters import TerminalFormatter
>>> from pygments.lexers import PostgresLexer
>>> from sqlparse import format
>>> from inventory.models import Brand

>>> Brand.objects.all().delete()
>>> Brand.objects.create(brand_id=1, name='nike')
>>> x = Brand.objects.filter(brand_id=1)
>>> sqlformatted = format(str(x.query), reindent=True)
>>> print(highlight(sqlformatted, PostgresLexer(), TerminalFormatter()))
# SELECT "inventory_brand"."brand_id",
#        "inventory_brand"."name",
#        "inventory_brand"."nickname"
# FROM "inventory_brand"
# WHERE "inventory_brand"."brand_id" = 1
```

### Aggregated
```python
>>> Brand.objects.all().count()
>>> reset_queries()
```