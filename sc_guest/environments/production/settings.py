from sc_guest.settings import *

DEBUG = False
ALLOWED_HOSTS = ['shippingcontainerhotel.gtriip.com', '13.213.145.234']
WSGI_APPLICATION = 'sc_guest.environments.production.wsgi.application'


# Security
# lib/python3.x/site-packages/django/conf/global_settings.py

# X_FRAME_OPTIONS             = 'DENY'
# SESSION_COOKIE_SECURE       = True
# SESSION_COOKIE_HTTPONLY     = True
# CSRF_COOKIE_SECURE          = True
# CSRF_COOKIE_HTTPONLY        = True
# SECURE_BROWSER_XSS_FILTER   = True
# SECURE_SSL_REDIRECT         = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "guest_static/")
STATIC_URL = '/guest_static/'

# Guest Facing
GUEST_ENDPOINT = [
    {
        'id': 'zr1',
        'name': 'Container No 1 @ Haw Par Villa',
        'description': 'Container No 1 @ Haw Par Villa',
        'image': '/guest_static/img/property/Zehnder-Road1.jpg',
        'address': 'LOT 02781W MK 03 262 Pasir Panjang Road, Singapore 118628',
        #'url': 'http://192.168.1.100:8085',
        # 'url': 'https://shippingcontainerhotelqa.gtriip.com:8443/container/81ks',
        'url': 'http://app-zr1:8082',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 60,
    },
    {
        'id': 'zr2',
        'name': 'Container No 2 @ Haw Par Villa',
        'description': 'Container No 2 @ Haw Par Villa',
        'image': '/guest_static/img/property/Zehnder-Road2.jpg',
        'address': 'LOT 02781W MK 03 262 Pasir Panjang Road, Singapore 118628',
        #'url': 'http://192.168.1.100:8085',
        # 'url': 'https://shippingcontainerhotelqa.gtriip.com:8443/container/81ks',
        'url': 'http://app-zr2:8083',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 60,
    },
    {
        'id': '77ks',
        'name': '77 KontainerSpace',
        'description': 'Shipping Container Hotel @ Block 77 Ayer Rajah Crescent (No.1)',
        'image': '/guest_static/img/property/BLK77-container-hotels.jpg',
        'address': '77 Ayer Rajah Crescent, Singapore 139952',
        #'url': 'http://192.168.1.100:8085',
        # 'url': 'https://shippingcontainerhotelqa.gtriip.com:8443/container/77ks',
        'url': 'http://app-77ks:8080',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 60,
    },
    {
        'id': '81ks',
        'name': '81 KontainerSpace',
        'description': 'Shipping Container Hotel @ Block 81 Ayer Rajah Crescent (No.2)',
        'image': '/guest_static/img/property/BLK81-container-hotels.jpg',
        'address': '81 Ayer Rajah Crescent, Singapore 139952',
        #'url': 'http://192.168.1.100:8085',
        # 'url': 'https://shippingcontainerhotelqa.gtriip.com:8443/container/81ks',
        'url': 'http://app-81ks:8081',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 60,
    },
]


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

# google analytics measurement id
GA_MEASUREMENT_ID   = 'G-VLVYMFJ35W'
# link to access static images, configured on webserver
STATIC_IMAGE_URL    = '/guest_static/img'

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
        'room_image': '/guest_static/img/room/shipping-container-room.jpg',
    },
    {
        'room_type' : 'Container No 2 @ Haw Par Villa',
        'room_name' : 'Container No 2 @ Haw Par Villa',
        'room_image': '/guest_static/img/room/shipping-conatiner-room.jpg',
    }
]
