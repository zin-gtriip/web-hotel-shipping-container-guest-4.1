"""
Django settings for sc_guest project.

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
    'custom',
    'guest_facing.registration',
    'guest_facing.check_out',
    'guest_facing.chat',
    'guest_facing.core',
    'captcha',
    'django_user_agents',
    'django_countries',
    'widget_tweaks',
    'compressor',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
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

ROOT_URLCONF = 'sc_guest.urls'

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

WSGI_APPLICATION = 'sc_guest.wsgi.application'


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

TIME_ZONE = 'Asia/Singapore'

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


# Endpoint configuration
# Token
TOKEN_ENDPOINT = [
    {
        'type': 'guest_facing',
        'url': 'http://app-77ks:8080/',
        'username': 'web-guest-client',
        'password': 'HotelTemplate1234',
        'timeout': 30,
    },
    {
        'type': 'amp',
        'url': 'http://app-77ks:8080/',
        'username': 'web-amp-client',
        'password': 'HotelTemplate1234',
        'timeout': 30,
    },
     {
        'type': 'guest_facing',
        'url': 'http://app-81ks:8081/',
        'username': 'web-guest-client',
        'password': 'HotelTemplate1234',
        'timeout': 30,
    },
    {
        'type': 'amp',
        'url': 'http://app-81ks:8081/',
        'username': 'web-amp-client',
        'password': 'HotelTemplate1234',
        'timeout': 30,
    }
]
# Guest Facing
GUEST_ENDPOINT = [
    {
        'id': '77ks',
        'name': '77 KontainerSpace',
        'description': 'Shipping Container Hotel @ Block 77 Ayer Rajah Crescent (No.1)',
        'image': '/static/img/property/BLK77-container-hotels.jpg',
        'address': '77 Ayer Rajah Crescent, Singapore 139952',
        'url': 'http://app-77ks:8080/',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 30,
    },
    {
        'id': '81ks',
        'name': '81 KontainerSpace',
        'description': 'Shipping Container Hotel @ Block 81 Ayer Rajah Crescent (No.2)',
        'image': '/static/img/property/BLK81-container-hotels.jpg',
        'address': '81 Ayer Rajah Crescent, Singapore 139952',
        'url': 'http://app-81ks:8081/',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 30,
    }
]
# AMP
AMP_ENDPOINT = [
    {
        'id': '77ks',
        'name': '77 KontainerSpace',
        'url': 'http://app-77ks:8080/',
        'key': '686d2f8f0e0765da0dfd7e40a748bc2eec02b2a0bcb097d5685c18965eb26469e307065b61bd14734122874f6431c4a30b471cf31342902f99eff49922545717',
        'timeout': 30,
    },
    {
        'id': '81ks',
        'name': '81 KontainerSpace',
        'url': 'http://app-81ks:8081/',
        'key': '686d2f8f0e0765da0dfd7e40a748bc2eec02b2a0bcb097d5685c18965eb26469e307065b61bd14734122874f6431c4a30b471cf31342902f99eff49922545717',
        'timeout': 30,
    }
]


# OCR Endpoint configuration
OCR_ENDPOINT_URL                = 'https://cv.gtriip.com/recognition/'
OCR_ENDPOINT_KEY                = 'rvH7MT70.7RoZxH8gtBfPgZt7kgNxRtybwq3Gp4vW'
OCR_ENDPOINT_TIMEOUT_LIMIT      = 60


# Messaging configuration
#QA
CHAT_SUB_KEY            = 'sub-c-8994bb8a-11ec-11ec-8a3e-d2716870c3f2'
CHAT_PUB_KEY            = 'pub-c-1b823142-c442-42e7-963a-d529c1f373ce'
CHAT_SEC_KEY            = 'sec-c-NDk2YTY2NDAtYmExOC00MGU1LTliYmItMWFmMzA0NGE3OTg5'
CHAT_UUID               = 'FO' # no special character, including space
CHAT_AUTO_START_TIME    = '18:00'
CHAT_AUTO_END_TIME      = '09:00'


# Maximum size in bytes of request data (excluding file uploads) that will be
# read before a SuspiciousOperation (RequestDataTooBig) is raised.
# will be used when sending passport image to backend processing

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760 # 10 MB


# Encrypt and decrypt key using cryptography lib
# https://pypi.org/project/cryptography/

FERNET_KEY = b'aJAwfZCJTITCVp-76x9_z8aaFSAFvlrOIFRQEDLm6p8='


# Google Recaptcha configuration
# https://pypi.org/project/django-recaptcha/

RECAPTCHA_PUBLIC_KEY        = '6Lc5PcgaAAAAAJ4kwMRjpH5kdt48_lwi48kpkR1w'
RECAPTCHA_PRIVATE_KEY       = '6Lc5PcgaAAAAAGDC4DyZzx9uhA3t5yiUNMpAKJOh'


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
#             'filename': BASE_DIR +'/logs/info.log',
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
HOTEL_NAME          = 'KontainerSpace'
GST_NO              = 'A13572468B'
BUSINESS_NO         = '975308642Z'
CURRENCY_SYMBOL     = 'S$'
TNC_LINK            = 'https://hotels.cloudbeds.com/reservation/PK9fOV'
PRIVACY_LINK        = 'https://hotels.cloudbeds.com/reservation/PK9fOV'
HOST_URL            = 'https://kontainerspaceqa.gtriip.com'
APP_IOS_URL         = 'http://itunes.apple.com'
APP_ANDROID_URL     = 'http://play.google.com/store/apps'
APP_DIRECT_URL      = 'https://www.google.com'
# google analytics measurement id
GA_MEASUREMENT_ID   = 'G-XXK7VS7S3V'
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
        'room_type' : 'Shipping Container Hotel @ Block 81',
        'room_name' : 'Shipping Container Hotel @ Block 81',
        'room_image': '/static/img/room/shipping-container-room.jpg',
    },
    {
        'room_type' : 'Shipping Container Hotel @ Block 77',
        'room_name' : 'Shipping Container Hotel @ Block 77',
        'room_image': '/static/img/room/shipping-conatiner-room.jpg',
    }
]
# default age limit for adult, if AMP is not provided
REGISTRATION_ADULT_AGE_LIMIT = 18
# registration pages that has expiry session (timer), make sure these are registration url
REGISTRATION_EXPIRY_SESSION_PAGES = [
    'reservation',
    'guest_list',
    'detail',
    'ocr',
    'other_info',
]
# registration views that use `parameter_required` validation
REGISTRATION_PARAMETER_REQUIRED_PAGES = [
    'reservation',
    'guest_list',
    'other_info',
    'complete',
]
# progress bar rate on registration page
REGISTRATION_PROGRESS_BAR_START_RATE = 10
REGISTRATION_PROGRESS_BAR_END_RATE = 100
REGISTRATION_PROGRESS_BAR_PAGES = [
    'login',
    'reservation',
    'guest_list',
    'other_info',
    'complete',
]
# progress bar rate calculation, -1 to exclude first page
REGISTRATION_PROGRESS_BAR_RATE_PER_PAGE = (REGISTRATION_PROGRESS_BAR_END_RATE - REGISTRATION_PROGRESS_BAR_START_RATE) / (len(REGISTRATION_PROGRESS_BAR_PAGES) - 1)
# complete email template directory
REGISTRATION_COMPLETE_EMAIL = 'registration/email/complete.html'
# determine default mandatory of ocr field in detail page, if AMP is not provided
REGISTRATION_OCR = True
