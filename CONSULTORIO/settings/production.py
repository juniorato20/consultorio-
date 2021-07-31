from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['consultoriodecitas.herokuapp.com']


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd5qpo4mtrmi8u5',
        'USER' : 'lfdfouoshcuxcp',
        'PASSWORD' : '4d5b12a888ccd6ed1ceae79a3aff11ba947570984f0540cd6e39112ee9b33f9a',
        'HOST' : 'ec2-35-168-145-180.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}


STATICFILES_DIRS = (BASE_DIR,'static')