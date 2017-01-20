DEBUG = True
TEMPLATE_DEBUG = DEBUG
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_PATH, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
STATIC_ROOT = ''
STATIC_URL = '/static/'

DEBUG = True
TEMPLATE_DEBUG = True

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'charts/'),
    os.path.join(PROJECT_PATH, 'fiber_mode/'),  
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'charts',
    'fiber_mode',
)

SECRET_KEY = '5ry^!i1c6y*$396rb@^ibm1m%eg-aaw8mf0qurk%+a3-r5woo)'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

TEMPLATES = [
    {
        'DIRS': ['/home/marcin/topt/fiber_mode/charts/', 'charts', 'fiber_mode'],
    },
]


ROOT_URLCONF = 'charts.urls'

WSGI_APPLICATION = 'charts.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'charts',

)
