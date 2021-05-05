from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['consultorioodontologico.herokuapp.com']


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ddtlvkaigh28va',
        'USER' : 'wksaantkstodfe',
        'PASSWORD' : 'afe49a3b46b439f0735d7ac2f3c152f39e0d4296cc077e246d541383b3a09183',
        'HOST' : 'ec2-54-163-254-204.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

