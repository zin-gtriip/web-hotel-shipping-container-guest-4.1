from hotel_guest.settings import *

DEBUG = False
WSGI_APPLICATION = 'hotel_guest.environments.prod_wsgi.application'
