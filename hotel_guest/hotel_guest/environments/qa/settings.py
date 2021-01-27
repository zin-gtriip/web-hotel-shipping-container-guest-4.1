from hotel_guest.settings import *

DEBUG = False
ALLOWED_HOSTS = ['hoteltemplateqa.gtriip.com']
WSGI_APPLICATION = 'hotel_guest.environments.qa.wsgi.application'


# Security
# lib/python3.x/site-packages/django/conf/global_settings.py

X_FRAME_OPTIONS             = 'DENY'
SESSION_COOKIE_SECURE       = True
SESSION_COOKIE_HTTPONLY     = True
CSRF_COOKIE_SECURE          = True
CSRF_COOKIE_HTTPONLY        = True
SECURE_BROWSER_XSS_FILTER   = True
SECURE_SSL_REDIRECT         = True
