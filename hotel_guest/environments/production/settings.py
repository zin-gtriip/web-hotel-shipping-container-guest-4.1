from hotel_guest.settings import *

DEBUG = False
WSGI_APPLICATION = 'hotel_guest.environments.production.wsgi.application'