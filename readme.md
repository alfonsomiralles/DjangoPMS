# Django Project - PMS

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

# I will use django-seed to seed the database with fake information. This is the github of the library
https://github.com/Brobin/django-seed

# to init the server
python manage.py runserver


# to create a superuser for Django Admin Panel
python manage.py createsuperuser

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)