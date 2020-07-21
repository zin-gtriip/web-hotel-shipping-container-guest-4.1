"""
A set of custom request processors that return dictionaries to every request &
template. Each function takes the request object as its only parameter and
returns a dictionary to add to the context.

For more information, visit link below:
https://stackoverflow.com/a/433209
"""

from django.contrib.sessions.models import Session

def session(request):
    """Returns pre-arrival expiry date"""
    expire_date = request.session.get('pre_arrival', {}).get('expiry_date', '')
    return {'PRE_ARRIVAL_EXPIRY_DATE': expire_date}
