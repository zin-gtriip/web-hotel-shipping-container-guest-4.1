"""
A set of custom request processors that return dictionaries to every request &
template. Each function takes the request object as its only parameter and
returns a dictionary to add to the context.

For more information, visit link below:
https://stackoverflow.com/a/433209
"""

from django.contrib.sessions.models import Session

def session(request):
    """Returns session expiry date"""
    expire_date = ''
    if request.session.session_key:
        session = Session.objects.get(session_key=request.session.session_key)
        expire_date = session.expire_date
    return {'SESSION_EXPIRY_DATE': expire_date}
