from sc_guest.settings import *

DEBUG = False
#ALLOWED_HOSTS = ['trevo.gtriip.com']
ALLOWED_HOSTS = ['shippingcontainerhotelqa.gtriip.com']
WSGI_APPLICATION = 'sc_guest.environments.qa.wsgi.application'


# Security
# lib/python3.x/site-packages/django/conf/global_settings.py

X_FRAME_OPTIONS             = 'DENY'
SESSION_COOKIE_SECURE       = True
SESSION_COOKIE_HTTPONLY     = True
CSRF_COOKIE_SECURE          = True
CSRF_COOKIE_HTTPONLY        = True
SECURE_BROWSER_XSS_FILTER   = True
SECURE_SSL_REDIRECT         = True


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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "guest_static/")
STATIC_URL = '/guest_static/'

# room mapping, use `room_type` as identifier
REGISTRATION_ROOM_TYPES = [
    {
        'room_type' : 'Deluxe',
        'room_name' : 'Deluxe Room',
        'room_image': '/guest_static/img/room/room-deluxe.jpg',
    },
    {
        'room_type' : 'Shipping Container Hotel @ Block 81',
        'room_name' : 'Shipping Container Hotel @ Block 81',
        'room_image': '/guest_static/img/room/shipping-container-room.jpg',
    },
    {
        'room_type' : 'Shipping Container Hotel @ Block 77',
        'room_name' : 'Shipping Container Hotel @ Block 77',
        'room_image': '/guest_static/img/room/shipping-conatiner-room.jpg',
    },
    {
        'room_type' : 'Container No 1 @ Haw Par Villa',
        'room_name' : 'Container No 1 @ Haw Par Villa',
        'room_image': '/guest_static/img/room/container_1.jpg',
    },
    {
        'room_type' : 'Container No 2 @ Haw Par Villa',
        'room_name' : 'Container No 2 @ Haw Par Villa',
        'room_image': '/guest_static/img/room/container_2.jpg',
    }
]

# google analytics measurement id
GA_MEASUREMENT_ID   = 'G-0QBWCB1WQ2'

