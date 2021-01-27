"""
A set of custom request processors that return dictionaries to every request &
template. Each function takes the request object as its only parameter and
returns a dictionary to add to the context.

For more information, visit link below:
https://stackoverflow.com/a/433209
"""

from django.conf import settings

def hotel_conf(request):
    """Returns hotel name"""
    return {'HOTEL_NAME': settings.HOTEL_NAME}
