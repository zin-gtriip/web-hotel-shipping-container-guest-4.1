"""
A set of custom request processors that return dictionaries to every request &
template. Each function takes the request object as its only parameter and
returns a dictionary to add to the context.

For more information, visit link below:
https://stackoverflow.com/a/433209
"""
from core import utils as core_utils


def session(request):
    """Returns pre-arrival expiry date and duration"""
    session_key = request.session.session_key or ''
    initial_expiry_date = request.session.get('pre_arrival', {}).get('initial_expiry_date', '')
    token_id = core_utils.encrypt(session_key + initial_expiry_date)
    initial_expiry_duration = request.session.get('pre_arrival', {}).pop('initial_expiry_duration', '') # use once only, otherwise considered new session
    return {'SESSION_EXTEND_TOKEN_ID': token_id, 'SESSION_INITIAL_EXPIRY_DURATION': initial_expiry_duration}
