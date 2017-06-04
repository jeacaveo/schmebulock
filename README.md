mkvirtualenv schmebulock
workon schmebulock

pip install -r requirements.txt

To configure initial database:
    create database schmebulock;
    create user schmebulock with password 'schmebulock';
    alter role schmebulock set client_encoding to 'utf8';
    alter role schmebulock set default_transaction_isolation to 'read committed';
    alter role schmebulock set timezone to 'UTC'
    grant all privileges on database schmebulock to schmebulock;

python manage.py migrate

python manage.py createsuperuser
Admin credentials:
    Username: admin
    Password: admin123

Tests:

python manage.py test [APP_NAME][.TEST_MODULE][:TestClass][.TEST_NAME]

Coverage:

coverage run --source='PATH_TO_APP_PROJECT_DIRECTORY' manage.py test  [APP_NAME][.TEST_MODULE][:TestClass][.TEST_NAME]
