# Notes
Django Database ORM Mastery 2024\
https://www.udemy.com/course/django-4x-orm-mastery

### Commands
Create Django Project\
`$ django-admin startproject core .`\
`$ django-admin startproject ecommerce .`

Create Django Application\
`$ python3 manage.py startapp newapp`\
`$ python3 manage.py startapp newapp ./core/newapp`\
`$ python3 manage.py startapp inventory`

Run Django Server\
`$ python3 manage.py runserver`\
`$ python3 manage.py runserver 8080`

### Overview (Projects vs Apps)
- Core Project
    - Product App
    - Customers App
    - Checkout App

### Migrations & Management (sqlite3)
`$ python3 manage.py makemigrations`\
`$ python3 manage.py migrate`\
`$ python3 manage.py showmigrations --list`\
`$ python3 manage.py migrate inventory 0002_alter_attribute_name`\
`$ python3 manage.py migrate inventory zero`\
`$ python3 manage.py createsuperuser`

### VSCode Extensions
- SQLite
- Pylint
- Pylance
- Black Formatter
- Flake8
- Ruff

### Other
- LucidChart is a good Diagram Software