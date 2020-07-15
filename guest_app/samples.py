from django.utils.translation   import gettext, gettext_lazy as _

check_in_get_data = [
    {
        'reservation_no': '1234',
        'arrival_date': '2020-06-01',
        'last_name': 'TEST',
        'first_name': 'TEST',
        'passport_no': '12345',
        'nationality': 'SG',
        'birth_date': '1995-07-15',
        'adult_number': '2',
        'child_number': '1',
        'email': 'test@test.com',
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
        ],
    },
    {
        'reservation_no': '12345',
        'arrival_date': '2020-06-01',
        'last_name': 'TEST',
    }
]

def get_data(post_data):
    sample_data = next((data for data in check_in_get_data \
        if data['reservation_no'] == post_data['reservation_no'] and \
        data['arrival_date'] == str(post_data['arrival_date']) and \
        data['last_name'] == str(post_data['last_name'])), {})
    if sample_data:
        sample_data['status'] = 'success'
    else:
        sample_data = {'status': 'error', 'message': _('Error connecting to server')}
    return sample_data


check_in_post_data = {
    'status': 'success',
    'reservations': [
        {
            'identifier': '2',
            'room_type': 'Premier Room',
            'check_in_date': 'Thu, 12/06/20',
            'check_out_date': 'Mon, 18/06/20',
        }
    ],
}

def send_data(post_data):
    return check_in_post_data
