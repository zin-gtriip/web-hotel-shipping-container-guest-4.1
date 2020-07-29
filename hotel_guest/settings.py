"""
Django settings for hotel_guest project.

Generated by 'django-admin startproject' using Django 2.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v-g1k*x-9fnj&w)x&(-oawy5lg698)+%og#33smma)^fr87u18'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'widget_tweaks',
    'django_cron',
    'django_countries',
    'django_user_agents',
    'guest_base.apps.GuestBaseConfig',
    'pre_arrival.apps.PreArrivalConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'hotel_guest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'guest_base.context_processors.hotel_conf',
                'pre_arrival.context_processors.session',
            ],
        },
    },
]

WSGI_APPLICATION = 'hotel_guest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Available languages for translation
# https://samulinatri.com/blog/django-translation/

LANGUAGES = [
    ('en', 'EN'),
    ('ja', 'JP'),
    ('zh-hans', 'ZH'),
]


# Prioritize locale path to override default translation
# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-LOCALE_PATHS

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'


# django-compressor setting for compressing file
# this setting will be changed to True by default, if running in PROD mode and COMPRESS_ENABLED is not defined

# COMPRESS_ENABLED = True


# Static files finders for django-compressor
# https://django-compressor.readthedocs.io/en/stable/quickstart/#installation

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


# Compressor settings for css file. JS file is compressed by default
# https://django-compressor.readthedocs.io/en/stable/settings/#django.conf.settings.COMPRESS_CSS_FILTERS

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSCompressorFilter',
]


# SASS complier for django_libsass
# https://github.com/torchbox/django-libsass

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


# Gateway API configuration

GATEWAY_API_HOST    = 'http://175.41.166.197:8080/hotelTemplate'
GATEWAY_API_KEY     = '9a051acd7c9946dfbc7aa21139572824'
# GATEWAY_API_HASH    = '6C209DED142B90DA15A65F129CFCB281108A9D4373E04C19C03719C3E5F1DB0EB538C'
# GATEWAY_HOTEL_ID    = '13B76FAC767FAD58C03891014D8C2DF7B044D84DFDC870F76E80D577271E381D1FF5AD189FA3E37AD886BE2FD11027A8F263AFEFA999B97535CA4CC6615C5D6B'
# GATEWAY_LANGUAGE_ID = '4'


# Cron job configuration
# Also need to setup scheduled cron on server, ex crontab on Unix
# https://django-cron.readthedocs.io/en/latest/

CLEAR_SESSION_CRON_JOB_RUN_TIME = '00:00'
CRON_CLASSES = [
    "pre_arrival.cron_jobs.ClearSessionCronJob",
]


# Other configuration
# General
# page title on every page
HOTEL_NAME          = 'GTRIIP'
# default django variable for date format
DATE_INPUT_FORMATS  = ['%Y-%m-%d']

# Pre Arrival
# expiration time for the pre-arrival (in minutes)
PRE_ARRIVAL_AGE     = 15
# room mapping, use `room_type` as identifier
ROOM_TYPES = [
    {
        'room_type' : 'Premier',
        'room_name' : 'Premier Room',
        'room_image': 'premier.jpg',
    },
    {
        'room_type' : 'Deluxe',
        'room_name' : 'Deluxe Room',
        'room_image': 'deluxe.jpg',
    },
    {
        'room_type' : 'Villa',
        'room_name' : 'Villa',
        'room_image': 'villa.jpg',
    },
]
# age limit of ocr validation
PASSPORT_AGE_LIMIT      = 18
# age limit of detail form that should count as adult or child
DETAIL_FORM_AGE_LIMIT   = 13
# progress bar rate on pre-arrival page
PROGRESS_BAR_START_RATE = 10
PROGRESS_BAR_END_RATE   = 100
# urls that use progress bar
PRE_ARRIVAL_URLS = [
    'login',
    'reservation',
    'passport',
    'detail',
    'other_info',
    'complete',
]