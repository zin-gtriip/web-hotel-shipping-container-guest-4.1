from django.utils.translation   import gettext, gettext_lazy as _

check_in_data = [
    {
        'confirmation_number': '1234',
        'arrival_date': '2020-04-01',
        'last_name': 'TEST',
    },
    {
        'confirmation_number': '12345',
        'arrival_date': '2020-04-01',
        'last_name': 'TEST',
    }
]

def get_data(post_data):
    sample_data = next((data for data in check_in_data \
        if data['confirmation_number'] == post_data['confirmation_number'] and \
        data['arrival_date'] == str(post_data['arrival_date']) and \
        data['last_name'] == str(post_data['last_name'])), {})
    if sample_data:
        sample_data['status'] = 'success'
    else:
        sample_data = {'status': 'error', 'message': _('Error connecting to server')}
    return sample_data