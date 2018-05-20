import os

DEBUG = False
SECRET_KEY = '1234'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('/var/cdn', 'db.sqlite3'),
    }
}