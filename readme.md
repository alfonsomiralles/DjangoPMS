# Django Property Management System

This is a Django project

## Installation

Use this to install Django

```bash
python -m pip install Django
```

## Usage

```python
# to create the project
django-admin startproject <name of the project>

# into the project folder, to init the database
python manage.py migrate

# If we want to create an app, instead of the previous step we will use
python manage.py startapp <name of the app>
# Then, into the settings.py add the <name of the app> into the INSTALLED_APPS directory. To check if everything is correct
python manage.py check <name of the app>
# If we do any changes in models.py we need to check and create the table in the database with
python manage.py makemigrations
python manage.py migrate


# to init the server
python manage.py runserver

#to create superuser
python manage.py createsuperuser

```

## License
[MIT](https://choosealicense.com/licenses/mit/)