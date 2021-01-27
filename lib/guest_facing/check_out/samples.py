check_out_login_all = {
    "status_code": 500,
    "data": [
        {
            "reservation_no": "EARYE",
            "first_name": "Mariano",
            "last_name": "Test"
        },
        {
            "reservation_no": "B09AB",
            "first_name": "Sook",
            "last_name": "Test"
        }
    ]
}

check_out_login_1 = {
    'status_code': 500,
    'data': [
        {
            "reservation_no": "B09AB",
            "first_name": "Sook",
            "last_name": "Test"
        }
    ]
}

check_out_login_2 = {
    'status_code': 500,
    'data': []
}

def get_login(**kwargs):
    identifier = kwargs.get('id')
    if identifier == 'all':
        return check_out_login_all
    elif identifier == 1:
        return check_out_login_1
    else:
        return check_out_login_2


check_out_bill_all = {
    "reservation_info": [
        {
            "reservation_no": "EARYE",
            "first_name": "Mariano",
            "last_name": "Test",
            "arrival_date": "2020-10-30",
            "departure_date": "2020-10-31",
            "room_no": "3010K",
            "room_type": "Premier",
            "adults": 2,
            "children": 0,
            "check_out_status": 500,
            "item_total_amount": 2199.0,
            "tax_amount": 200.98,
            "grand_total": 2399.98,
            "items": [
                {
                    "date": "2020-10-30",
                    "item_name": "Item X",
                    "amount": 600.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Y",
                    "amount": 400.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Z",
                    "amount": 99.5
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item X",
                    "amount": 600.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Y",
                    "amount": 400.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Z",
                    "amount": 99.5
                }
            ]
        },
        {
            "reservation_no": "B09AB",
            "first_name": "Sook",
            "last_name": "Test",
            "arrival_date": "2020-10-30",
            "departure_date": "2020-10-31",
            "room_no": "3010K",
            "room_type": "Deluxe",
            "adults": 2,
            "children": 0,
            "check_out_status": 500,
            "item_total_amount": 2199.0,
            "tax_amount": 200.98,
            "grand_total": 2399.98,
            "items": [
                {
                    "date": "2020-10-30",
                    "item_name": "Item X",
                    "amount": 600.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Y",
                    "amount": 400.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Z",
                    "amount": 99.5
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item X",
                    "amount": 600.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Y",
                    "amount": 400.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Z",
                    "amount": 99.5
                }
            ]
        }
    ],
    "total_amount": 4799.96,
    "overall_status": True
}

check_out_bill_1 = {
    "reservation_info": [
        {
            "reservation_no": "EARYE",
            "first_name": "Mariano",
            "last_name": "Test",
            "arrival_date": "2020-10-30",
            "departure_date": "2020-10-31",
            "room_no": "3010K",
            "room_type": "Premier",
            "adults": 2,
            "children": 0,
            "check_out_status": 500,
            "item_total_amount": 2199.0,
            "tax_amount": 200.98,
            "grand_total": 2399.98,
            "items": [
                {
                    "date": "2020-10-30",
                    "item_name": "Item X",
                    "amount": 600.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Y",
                    "amount": 400.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Z",
                    "amount": 99.5
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item X",
                    "amount": 600.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Y",
                    "amount": 400.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Z",
                    "amount": 99.5
                }
            ]
        },
    ],
    "total_amount": 4799.96,
    "overall_status": True
}

check_out_bill_2 = {
    "reservation_info": [
        {
            "reservation_no": "B09AB",
            "first_name": "Sook",
            "last_name": "Test",
            "arrival_date": "2020-10-30",
            "departure_date": "2020-10-31",
            "room_no": "3010K",
            "room_type": "Deluxe",
            "adults": 2,
            "children": 0,
            "check_out_status": 500,
            "item_total_amount": 2199.0,
            "tax_amount": 200.98,
            "grand_total": 2399.98,
            "items": [
                {
                    "date": "2020-10-30",
                    "item_name": "Item X",
                    "amount": 600.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Y",
                    "amount": 400.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Z",
                    "amount": 99.5
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item X",
                    "amount": 600.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Y",
                    "amount": 400.0
                },
                {
                    "date": "2020-10-30",
                    "item_name": "Item Z",
                    "amount": 99.5
                }
            ]
        }
    ],
    "total_amount": 4799.96,
    "overall_status": True
}

check_out_bill_3 = {
    "status_code": 100,
    "data": {
        "reservation_info": [],
        "total_amount": 0.0,
        "overall_status": True
    }
}

def get_bill(**kwargs):
    reservations_no = kwargs.get('reservation_no')
    if len(reservations_no) > 1:
        return check_out_bill_all
    elif reservations_no == ['EARYE']:
        return check_out_bill_1
    elif reservations_no == ['B09AB']:
        return check_out_bill_2
    else:
        return check_out_bill_3
