"""
A set of custom request processors that return dictionaries to every request &
template. Each function takes the request object as its only parameter and
returns a dictionary to add to the context.

For more information, visit link below:
https://stackoverflow.com/a/433209
"""


def session(request):
    """Returns pre-arrival expiry date"""
    initial_expiry_date = request.session.get('pre_arrival', {}).get('initial_expiry_date', '')
    extended_expiry_date = request.session.get('pre_arrival', {}).get('extended_expiry_date', '')
    return {'PRE_ARRIVAL_INITIAL_EXPIRY_DATE': initial_expiry_date, 'PRE_ARRIVAL_EXTENDED_EXPIRY_DATE': extended_expiry_date}
