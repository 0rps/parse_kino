from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xyz9txyq#k&1)1lkt!bsftb9a3!2ipld75d!dizw*5j)anc8r6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'KINODB_DEV',
        'PORT': 15432,
        'HOST': '127.0.0.1',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword'
    }
}
