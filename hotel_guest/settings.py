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
    'guest_facing.registration_adhoc_guest',
    'guest_facing.registration_ocr_required',
    'guest_facing.registration',
    'guest_facing.check_out',
    'guest_facing.core',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'compressor',
    'widget_tweaks',
    'django_countries',
    'django_user_agents',
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
                'guest_facing.core.context_processors.hotel_conf',
                'guest_facing.registration.context_processors.session',
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'


# Available languages for translation
# https://samulinatri.com/blog/django-translation/

LANGUAGES = [
    ('en', 'EN'),
    ('zh-hans', '华语'),
    ('ja', '日本語'),
]


# Prioritize locale path to override default translation
# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-LOCALE_PATHS

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


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


# Guest Facing Endpoint configuration

GUEST_ENDPOINT = [
    {
        'id': 'QAHotelProdSG11_1',
        'name': 'QA_Hotel_Prod_SG_3.0_1',
        'description': 'GTRIIP - Aurum',
        'image': '/static/img/property-1.jpg',
        'address': '1 East Street, Singapore',
        'url': 'http://hotel4qa.gtriip.com:8080/hotelTemplateProperty1',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 30,
    },
    {
        'id': 'QAHotelProdSG11_2',
        'name': 'QA_Hotel_Prod_SG_3.0_2',
        'description': 'GTRIIP - Nouveau',
        'image': '/static/img/property-2.jpg',
        'address': '1 South Beach Road, Singapore',
        'url': 'http://hotel4qa.gtriip.com:8080/hotelTemplateProperty2',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 30,
    },
]


# AMP Endpoint configuration

AMP_ENDPOINT = [
    {
        'id': 'QAHotelProdSG11_1',
        'name': 'QA_Hotel_Prod_SG_3.0_1',
        'url': 'http://hotel4qa.gtriip.com:8080/hotelTemplateProperty1',
        'key': '686d2f8f0e0765da0dfd7e40a748bc2eec02b2a0bcb097d5685c18965eb26469e307065b61bd14734122874f6431c4a30b471cf31342902f99eff49922545717',
        'timeout': 30,
    },
    {
        'id': 'QAHotelProdSG11_2',
        'name': 'QA_Hotel_Prod_SG_3.0_2',
        'url': 'http://hotel4qa.gtriip.com:8080/hotelTemplateProperty2',
        'key': '686d2f8f0e0765da0dfd7e40a748bc2eec02b2a0bcb097d5685c18965eb26469e307065b61bd14734122874f6431c4a30b471cf31342902f99eff49922545717',
        'timeout': 30,
    },
]


# OCR Endpoint configuration
OCR_ENDPOINT_URL                = 'https://ocr.gtriip.com/ocr/'
OCR_ENDPOINT_KEY                = 'F16430020E414D3CBB9FACB3DA8071F5'
OCR_ENDPOINT_TIMEOUT_LIMIT      = 60


# Maximum size in bytes of request data (excluding file uploads) that will be
# read before a SuspiciousOperation (RequestDataTooBig) is raised.
# will be used when sending passport image to backend processing

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760 # 10 MB


# Encrypt and decrypt key using cryptography lib
# https://pypi.org/project/cryptography/

FERNET_KEY = b'aJAwfZCJTITCVp-76x9_z8aaFSAFvlrOIFRQEDLm6p8='


# Logging
# https://docs.djangoproject.com/en/2.2/topics/logging/

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'simple': {
#             'format': '[%(asctime)s] %(message)s'
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': BASE_DIR +'/logs/log.log',
#             'maxBytes': 1024 * 1024 * 10, # 10MB
#             'backupCount': 10,
#             'formatter': 'simple',
#         },
#     },
#     'loggers': {
#         'gateways': { 'handlers': ['file'], 'level': 'INFO', 'propagate': True },
#         'django': { 'handlers': ['file'], 'level': 'ERROR', 'propagate': True },
#     },
# }


# Other configuration
# General
HOTEL_NAME          = 'GTRIIP'
GST_NO              = 'A13572468B'
BUSINESS_NO         = '975308642Z'
CURRENCY_SYMBOL     = 'S$'
TNC_LINK            = 'https://www.gtriip.com'
PRIVACY_LINK        = 'https://www.gtriip.com'
HOST_URL            = 'https://hoteltemplateqa.gtriip.com'
APP_IOS_URL         = 'http://itunes.apple.com'
APP_ANDROID_URL     = 'http://play.google.com/store/apps'
APP_DIRECT_URL      = 'https://www.google.com'
# link to access static images, configured on webserver
STATIC_IMAGE_URL    = '/static/img'
# default django variable for date format
DATE_INPUT_FORMATS  = ['%Y-%m-%d']
# set session to be saved everytime
SESSION_SAVE_EVERY_REQUEST = True

# Registration
# default expiry time for the registration (in minutes), if AMP is not provided
REGISTRATION_SESSION_AGE_INITIAL = 15
REGISTRATION_SESSION_AGE_EXTEND = 10
# room mapping, use `room_type` as identifier
REGISTRATION_ROOM_TYPES = [
    {
        'room_type' : 'Premier',
        'room_name' : 'Premier Room',
        'room_image': '/static/img/room-premier.jpg',
    },
    {
        'room_type' : 'Deluxe',
        'room_name' : 'Deluxe Room',
        'room_image': '/static/img/room-deluxe.jpg',
    },
    {
        'room_type' : 'Villa',
        'room_name' : 'Villa',
        'room_image': '/static/img/room-villa.jpg',
    },
]
# age limit for adult, used on passport, detail page
REGISTRATION_ADULT_AGE_LIMIT = 18
# registration pages that has expiry session (timer), make sure these are registration url
REGISTRATION_EXPIRY_SESSION_PAGES = [
    'reservation',
    'passport',
    'guest_list',
    'detail',
    'extra_passport',
    'other_info',
]
# registration views that use `parameter_required` validation
REGISTRATION_PARAMETER_REQUIRED_PAGES = [
    'reservation',
    'passport',
    'detail',
    'other_info',
    'complete',
]
# progress bar rate on registration page
REGISTRATION_PROGRESS_BAR_START_RATE = 10
REGISTRATION_PROGRESS_BAR_END_RATE = 100
REGISTRATION_PROGRESS_BAR_PAGES = [
    'login',
    'reservation',
    'passport',
    'detail',
    'other_info',
    'complete',
]
# progress bar rate calculation, -1 to exclude first page
REGISTRATION_PROGRESS_BAR_RATE_PER_PAGE = (REGISTRATION_PROGRESS_BAR_END_RATE - REGISTRATION_PROGRESS_BAR_START_RATE) / (len(REGISTRATION_PROGRESS_BAR_PAGES) - 1)
# complete email template directory
REGISTRATION_COMPLETE_EMAIL = os.path.join(BASE_DIR, 'registration', 'templates', 'registration', 'email', 'complete.html')
