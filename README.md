# Schmebulock
## Crowdsourced Price Comparison App

Schmebulock's goal is to gather information from products and compare their prices over time, so users can make educated decisions on how to spend their money.

Currently under early development (alpha).

Development being done in GitLab and GitHub (mirror) simultaneously.

## Development Environment Configuration

### Requirements

- PostgreSQL9.5+
- Python3.4+
- virtualenvwrapper (recommended, but any virtualenv manager will do)
- Unix based OS (instructions written for GNU/Linux systems)


0. Activate virtualenv:

        mkvirtualenv schmebulock --python=/usr/bin/python3 (if it doesn't exist)
        workon schmebulock

1. Clone this repo into your preferred directory:

    GitLab:
        git clone git@gitlab.com:jeacaveo/schmebulock.git

    GitHub:
        git clone git@github.com:jeacaveo/schmebulock.git

    Enter project root:
        cd schmebulock

2. Configure database:

        $ sudo su postgres
        $ psql
        # create database schmebulock;
        # create user schmebulock with password 'schmebulock';
        # alter role schmebulock set client_encoding to 'utf8';
        # alter role schmebulock set default_transaction_isolation to 'read committed';
        # alter role schmebulock set timezone to 'UTC';
        # grant all privileges on database schmebulock to schmebulock;
        # alter user schmebulock createdb;
        # \q
        $ exit

3. Install requirements:

        pip install -r requirements-dev.txt

4. Run migrations:

        python manage.py migrate

5. Run tests without coverage (parameters in [] are optional):

        python manage.py test [app_name][.test_module][.TestClass][.test_name]

6. Run tests with coverage:

        coverage run --source='.' manage.py test && coverage report -m

7. Create superuser (optional):

        python manage.py createsuperuser
    (complete user creation process, suggestions: admin/admin123)

8. Load initial data for stores and brands (optional, if run multiple times it will create duplicates):

        python manage.py loaddata stores
        python manage.py loaddata brands

9. Run the server:

        python manage.py runserver

## Base URLS

API root (Django Schema Browser):

    http://localhost:8000/api/

API documentation root (Swagger):

    http://localhost:8000/api/docs/
