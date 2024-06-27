# Example 83 and beyond
# These are the commands entered into `python3 manage.py shell`

from inventory.models import Brand
from django.db import connection, reset_queries

Brand.objects.all()
Brand.objects.all().delete()
Brand.objects.create(brand_id=1, name='nike')

pip install pygments sqlparse
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PostgresLexer
from sqlparse import format
from inventory.models import Brand

Brand.objects.all().delete()
Brand.objects.create(brand_id=1, name='nike')
Brand.objects.create(brand_id=2, name='reebok')
x = Brand.objects.filter(brand_id=1)
sqlformatted = format(str(x.query), reindent=True)
print(highlight(sqlformatted, PostgresLexer(), TerminalFormatter()))

x = Brand.objects.filter(brand_id=1).values()
print(x)
x = Brand.objects.filter(brand_id=1).values('name')
print(x)

x = Brand.objects.all()
for i in x:
    print(f"{i.brand_id}: {i.name}")

# Exercise 105