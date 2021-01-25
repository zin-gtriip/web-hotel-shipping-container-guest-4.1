"""
A set of custom request processors that return dictionaries to every request &
template. Each function takes the request object as its only parameter and
returns a dictionary to add to the context.

For more information, visit link below:
https://stackoverflow.com/a/433209
"""
from django.conf    import settings
from django.urls    import reverse
from core     		import utils as core_utils


def session(request):
    """Returns registration expiry date, duration, and pages that use expiry session"""
    # get token id
    session_key = request.session.session_key or ''
    initial_expiry_date = request.session.get('registration', {}).get('initial_expiry_date', '')
    token_id = core_utils.encrypt(session_key + initial_expiry_date)
    # get expiry duration
    initial_expiry_duration = request.session.get('registration', {}).pop('initial_expiry_duration', '') # use once only, otherwise considered new session
    # get expiry session pages
    expiry_pages = []
    for page in settings.REGISTRATION_EXPIRY_SESSION_PAGES:
        try:
            url = reverse('registration:'+ page)
        except:
            url = None
        if url:
            expiry_pages.append(url)
    return {'SESSION_EXTEND_TOKEN_ID': token_id, 'SESSION_INITIAL_EXPIRY_DURATION': initial_expiry_duration, 'SESSION_EXPIRY_PAGES': expiry_pages}
