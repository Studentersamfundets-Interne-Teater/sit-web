"""
Django settings for SITnett project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
try:
    from .local import *
    DEBUG = False
    ALLOWED_HOSTS = [
    'sit.samfundet.no',
    'localhost'
]
except ModuleNotFoundError:
    print("Production environment not found – using local debug settings")
    DEBUG = True
    SECRET_KEY = 'n%8)o@tq63(+aacvf2q-1hx%=mb!^@8d$rs8$pwvw0x0x9#7ko'   
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    ALLOWED_HOSTS = []

# SECURITY WARNING: don't run with debug turned on in production!


# Application definition

INSTALLED_APPS = [
    'SITdata',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SITnett.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SITnett.wsgi.application'


# FUNKSJONALITET
# Skru av og på funksjonalitet her:

class FEATURE_SETTINGS():
    TOGGLE_KONTAKT = True  # skrur på kontaktliste.
    TOGGLE_AR = True  # skrur på årsider (med gruppefoto, verv, produksjoner og hendelser for et gitt år).
    TOGGLE_MEDLEMMER = True  # skrur på medlemsoversikt og medlemssider.
    TOGGLE_PRODUKSJONER = True  # skrur på produksjonsoversikt og produksjonssider.
    TOGGLE_ARRANGEMENTER = False  # skrur på arrangementssider.
    TOGGLE_VERV = True  # skrur på vervoversikt og vervsider.
    TOGGLE_UTTRYKK = False  # skrur på uttrykksliste.
    TOGGLE_ARKIV = False  # skrur på arkivsida (med tidslinje over produksjoner, arrangementer, bilder og hendelser).
    TOGGLE_DOKUMENTER = False  # skrur på dokumentfunksjonalitet.
    TOGGLE_EDIT = True  # skrur på redigeringsfunksjonalitet.


FEATURES = FEATURE_SETTINGS()

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/graphics/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'graphics'),]

MEDIA_ROOT = os.path.join(BASE_DIR, 'files')
MEDIA_URL = '/files/'


# Format på tidsrelaterte felter:

DATETIME_FORMAT = r"d.m.Y \k\l\o\k\k\a H.i"
DATETIME_INPUT_FORMATS = ["%d.%m.%Y %H.%M"]
DATE_FORMAT = r"d.m.Y"
DATE_INPUT_FORMATS = ["%d.%m.%Y"]
TIME_FORMAT = r"H.i"
TIME_INPUT_FORMATS = ["%H.%M"]

MONTH_NAMES = {1:"januar",2:"februar",3:"mars",4:"april",5:"mai",6:"juni",7:"juli",
    8:"august",9:"september",10:"oktober",11:"november",12:"desember"}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'nb'

TIME_ZONE = 'Europe/Oslo'
USE_TZ = False

USE_L10N = False
USE_I18N = True


# Brukerkonto-relatert:

LOGIN_URL = '/konto/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]