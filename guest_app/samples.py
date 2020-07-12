from django.utils.translation   import gettext, gettext_lazy as _

check_in_data = [
    {
        'confirmation_number': '1234',
        'arrival_date': '2020-06-01',
        'last_name': 'TEST',
        'adult_number': '2',
        'child_number': '1',
        'reservations': [
            {
                'identifier': '1',
                'room_type': 'Deluxe Room',
                'check_in_date': 'Thu, 12/06/20',
                'check_out_date': 'Mon, 18/06/20',
            },
            {
                'identifier': '2',
                'room_type': 'Premier Room',
                'check_in_date': 'Thu, 12/06/20',
                'check_out_date': 'Mon, 18/06/20',
            }
        ]
    },
    {
        'confirmation_number': '12345',
        'arrival_date': '2020-06-01',
        'last_name': 'TEST',
    }
]

ocr_data = {
    'expired': 'false',
    'date_of_birth': '20/10/1990',
    'first_name': 'TEST1',
    'last_name': 'TEST',
    'nationality': 'IDN',
    'number': '12345'
}

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