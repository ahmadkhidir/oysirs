from main.settings.dev import *


DEBUG = False

ALLOWED_HOSTS = ['207.154.192.71']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True