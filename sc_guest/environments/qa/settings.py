from sc_guest.settings import *

DEBUG = True
#ALLOWED_HOSTS = ['trevo.gtriip.com']
ALLOWED_HOSTS = ['shippingcontainerhotelqa.gtriip.com', '54.179.10.115']
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

# Encrypt and decrypt key using cryptography lib
# https://pypi.org/project/cryptography/

FERNET_KEY = b'aJAwfZCJTITCVp-76x9_z8aaFSAFvlrOIFRQEDLm6p8='

# Google Recaptcha configuration
# https://pypi.org/project/django-recaptcha/

RECAPTCHA_PUBLIC_KEY        = '6LdqZQkeAAAAACnxvJknAwsmhuyp_ruaTJR1Qwp5'
RECAPTCHA_PRIVATE_KEY       = '6LdqZQkeAAAAAMikf9gRKddCYsZ5ggGKQ_nlZXL5'


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

STATIC_URL = '/guest_static/'

# Endpoint configuration
# Token
TOKEN_ENDPOINT = [
    {
        'type': 'guest_facing',
        #'url': 'http://192.168.1.100:8085/oauth/token',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/77ks/oauth/token',
        # 'url': 'http://app-77ks:8080/oauth/token',
        'username': 'web-guest-client',
        'password': 'HotelTemplate1234',
        'timeout': 60,
    },
    {
        'type': 'amp',
        #'url': 'http://192.168.1.100:8085/oauth/token',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/77ks/oauth/token',
        # 'url': 'http://app-77ks:8080/oauth/token',
        'username': 'web-amp-client',
        'password': 'HotelTemplate1234',
        'timeout': 60,
    },
    {
        'type': 'guest_facing',
        #'url': 'http://192.168.1.100:8085/oauth/token',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/81ks/oauth/token',
        # 'url': 'http://app-81ks:8081/oauth/token',
        'username': 'web-guest-client',
        'password': 'HotelTemplate1234',
        'timeout': 60,
    },
    {
        'type': 'amp',
        #'url': 'http://192.168.1.100:8085/oauth/token',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/81ks/oauth/token',
        # 'url': 'http://app-81ks:8081/oauth/token',
        'username': 'web-amp-client',
        'password': 'HotelTemplate1234',
        'timeout': 60,
    },
    {
        'type': 'guest_facing',
        #'url': 'http://192.168.1.100:8085/oauth/token',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/zr1/oauth/token',
        # 'url': 'http://app-zr1:8082/oauth/token',
        'username': 'web-guest-client',
        'password': 'HotelTemplate1234',
        'timeout': 60,
    },
    {
        'type': 'amp',
        #'url': 'http://192.168.1.100:8085/oauth/token',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/zr1/oauth/token',
        # 'url': 'http://app-zr1:8082/oauth/token',
        'username': 'web-amp-client',
        'password': 'HotelTemplate1234',
        'timeout': 60,
    },
    {
        'type': 'guest_facing',
        #'url': 'http://192.168.1.100:8085/oauth/token',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/zr2/oauth/token',
        # 'url': 'http://app-zr2:8083/oauth/token',
        'username': 'web-guest-client',
        'password': 'HotelTemplate1234',
        'timeout': 60,
    },
    {
        'type': 'amp',
        #'url': 'http://192.168.1.100:8085/oauth/token',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/zr2/oauth/token',
        # 'url': 'http://app-zr2:8083/oauth/token',
        'username': 'web-amp-client',
        'password': 'HotelTemplate1234',
        'timeout': 60,
    }
]


# Guest Facing
GUEST_ENDPOINT = [
    {
        'id': 'zr1',
        'name': 'Container No 1 @ Haw Par Villa',
        'description': 'Container No 1 @ Haw Par Villa',
        'image': '/guest_static/img/property/Zehnder-Road1.jpg',
        'address': 'LOT 02781W MK 03 262 Pasir Panjang Road, Singapore 118628',
        #'url': 'http://192.168.1.100:8085',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/zr1',
        #'url': 'http://app-zr1:8082',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 60,
        'live': True,
    },
    {
        'id': 'zr2',
        'name': 'Container No 2 @ Haw Par Villa',
        'description': 'Container No 2 @ Haw Par Villa',
        'image': '/guest_static/img/property/Zehnder-Road2.jpg',
        'address': 'LOT 02781W MK 03 262 Pasir Panjang Road, Singapore 118628',
        #'url': 'http://192.168.1.100:8085',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/zr2',
        #'url': 'http://app-zr2:8083',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 60,
        'live': True,
    },
    {
        'id': '77ks',
        'name': '77 KontainerSpace',
        'description': 'Shipping Container Hotel @ Block 77 Ayer Rajah Crescent (No.1)',
        'image': '/guest_static/img/property/BLK77-container-hotels.jpg',
        'address': '77 Ayer Rajah Crescent, Singapore 139952',
        #'url': 'http://192.168.1.100:8085',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/77ks',
        #'url': 'http://app-77ks:8080',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 60,
        'live': False,
    },
    {
        'id': '81ks',
        'name': '81 KontainerSpace',
        'description': 'Shipping Container Hotel @ Block 81 Ayer Rajah Crescent (No.2)',
        'image': '/guest_static/img/property/BLK81-container-hotels.jpg',
        'address': '81 Ayer Rajah Crescent, Singapore 139952',
        #'url': 'http://192.168.1.100:8085',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/81ks',
        #'url': 'http://app-81ks:8081',
        'key': '36b682152421c5fcc2afe49fdafc77f84b029254b77a8af4c680b919725e5fa80f65d09df3c6311fc8f40cac9cc7fbea6a7d8dff6368af7d638abf041bd6ae45',
        'timeout': 60,
        'live': False,
    },
]

# AMP
AMP_ENDPOINT = [
    {
        'id': '77ks',
        'name': '77 KontainerSpace',
        #'url': 'http://192.168.1.100:8085',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/77ks',
        # 'url': 'http://app-77ks:8080',
        'key': '686d2f8f0e0765da0dfd7e40a748bc2eec02b2a0bcb097d5685c18965eb26469e307065b61bd14734122874f6431c4a30b471cf31342902f99eff49922545717',
        'timeout': 60,
    },
    {
        'id': '81ks',
        'name': '81 KontainerSpace',
        #'url': 'http://192.168.1.100:8085',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/81ks',
        # 'url': 'http://app-81ks:8081',
        'key': '686d2f8f0e0765da0dfd7e40a748bc2eec02b2a0bcb097d5685c18965eb26469e307065b61bd14734122874f6431c4a30b471cf31342902f99eff49922545717',
        'timeout': 60,
    },
    {
        'id': 'zr1',
        'name': 'Container No 1 @ Haw Par Villa',
        #'url': 'http://192.168.1.100:8085',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/zr1',
        # 'url': 'http://app-zr1:8082',
        'key': '686d2f8f0e0765da0dfd7e40a748bc2eec02b2a0bcb097d5685c18965eb26469e307065b61bd14734122874f6431c4a30b471cf31342902f99eff49922545717',
        'timeout': 60,
    },
    {
        'id': 'zr2',
        'name': 'Container No 2 @ Haw Par Villa',
        #'url': 'http://192.168.1.100:8085',
        'url': 'https://shippingcontainerhotelqa.gtriip.com/container/zr2',
        # 'url': 'http://app-zr2:8083',
        'key': '686d2f8f0e0765da0dfd7e40a748bc2eec02b2a0bcb097d5685c18965eb26469e307065b61bd14734122874f6431c4a30b471cf31342902f99eff49922545717',
        'timeout': 60,
    }
]

# Messaging configuration
#QA
CHAT_SUB_KEY            = 'sub-c-8994bb8a-11ec-11ec-8a3e-d2716870c3f2'
CHAT_PUB_KEY            = 'pub-c-1b823142-c442-42e7-963a-d529c1f373ce'
CHAT_SEC_KEY            = 'sec-c-NDk2YTY2NDAtYmExOC00MGU1LTliYmItMWFmMzA0NGE3OTg5'
CHAT_UUID               = 'FO' # no special character, including space
CHAT_AUTO_START_TIME    = '18:00'
CHAT_AUTO_END_TIME      = '09:00'


STATIC_IMAGE_URL    = '/guest_static/img'

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

