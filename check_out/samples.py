check_out_login = {
    'status': 500,
    'data': [
        {
            "reservation_no": "1111",
            "first_name": "Columbus",
            "last_name": "Leonard"
        },
        {
            "reservation_no": "3333",
            "first_name": "Notcolumbus",
            "last_name": "Leonard"
        }
    ]
}


check_out_bill = {
    "status": 500,
    "data": {
        "item_total_amount": 134.03,
        "tax_amount": 13.43,
        "grand_total": 147.47,
        "check_out_ok": 1,
        "items": [
            {
                "date": "2020-07-14",
                "item_name": "food",
                "amount": 13.7
            },
            {
                "date": "2020-07-14",
                "item_name": "food",
                "amount": 10.0
            },
            {
                "date": "2020-07-15",
                "item_name": "special",
                "amount": 100.0
            },
            {
                "date": "2020-07-15",
                "item_name": "special-special",
                "amount": 100.0
            },
            {
                "date": "2020-07-15",
                "item_name": "food and drinks",
                "amount": 110.34
            }
        ]
    }
}

def get_bill(**kwargs):
    data = {}
    reservation_no = kwargs.get('reservation_no', '')
    if reservation_no == ['1111']:
        data['reservation_info'] = [{
            "reservation_no": "1111",
            "first_name": "Columbus",
            "last_name": "Leonard",
            "room_no": "A123",
            "arrival_date": "2020-09-01",
            "departure_date": "2020-09-10",
        }]
    elif reservation_no == ['3333']:
        data['reservation_info'] = [{
            "reservation_no": "3333",
            "first_name": "Notcolumbus",
            "last_name": "Leonard",
            "room_no": "B321", #B321
            "arrival_date": "2020-09-02",
            "departure_date": "2020-09-09",
        }]
    else:
        data['reservation_info'] = [
            {
                "reservation_no": "1111",
                "first_name": "Columbus",
                "last_name": "Leonard",
                "room_no": "A123",
                "arrival_date": "2020-09-01",
                "departure_date": "2020-09-10",
            },
            {
                "reservation_no": "3333",
                "first_name": "Notcolumbus",
                "last_name": "Leonard",
                "room_no": "B321", #B321
                "arrival_date": "2020-09-02",
                "departure_date": "2020-09-09",
            }
        ]
    check_out_bill['data'].update(**data)
    return check_out_bill
