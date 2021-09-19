from sc_guest.settings import *

DEBUG = True
#ALLOWED_HOSTS = ['trevo.gtriip.com']
ALLOWED_HOSTS = ['54.179.10.115']
WSGI_APPLICATION = 'sc_guest.environments.qa.wsgi.application'


# Security
# lib/python3.x/site-packages/django/conf/global_settings.py

#X_FRAME_OPTIONS             = 'DENY'
#SESSION_COOKIE_SECURE       = True
#SESSION_COOKIE_HTTPONLY     = True
#CSRF_COOKIE_SECURE          = True
#CSRF_COOKIE_HTTPONLY        = True
#SECURE_BROWSER_XSS_FILTER   = True
#SECURE_SSL_REDIRECT         = True


# Logging
# https://docs.djangoproject.com/en/2.2/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR +'/logs/info.log',
            'maxBytes': 1024 * 1024 * 10, # 10MB
            'backupCount': 10,
            'formatter': 'simple',
        },
    },
    'loggers': {
        'gateways': { 'handlers': ['file'], 'level': 'INFO', 'propagate': True },
        'django': { 'handlers': ['file'], 'level': 'ERROR', 'propagate': True },
    },
}