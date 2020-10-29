check_out_login_all = {
    'status_code': 500,
    'data': [
        {
            "reservation_no": "8125B",
            "first_name": "YS",
            "last_name": "Test"
        },
        {
            "reservation_no": "4FM1T",
            "first_name": "Shae",
            "last_name": "Test"
        }
    ]
}

check_out_login_1 = {
    'status_code': 500,
    'data': [
        {
            "reservation_no": "8125B",
            "first_name": "YS",
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
    if identifier == 1:
        return check_out_login_all
    elif identifier == 2:
        return check_out_login_1
    else:
        return check_out_login_2


check_out_bill_all = {
    "status_code": 500,
    "data": {
        "reservation_info": [
            {
                "reservation_no": "8125B",
                "first_name": "YS",
                "last_name": "Test",
                "arrival_date": "2020-10-28",
                "departure_date": "2020-10-29",
                "room_no": "1010",
                "room_type": "Premier",
                "adults": 2,
                "children": 0,
                "check_out_status": 500,
                "item_total_amount": 1099.5,
                "tax_amount": 100.49,
                "grand_total": 1199.99,
                "items": [
                    {
                        "date": "2020-10-28",
                        "item_name": "Item X",
                        "amount": 600.0
                    },
                    {
                        "date": "2020-10-28",
                        "item_name": "Item Y",
                        "amount": 400.0
                    },
                    {
                        "date": "2020-10-28",
                        "item_name": "Item Z",
                        "amount": 99.5
                    }
                ]
            },
            {
                "reservation_no": "4FM1T",
                "first_name": "Shae",
                "last_name": "Test",
                "arrival_date": "2020-10-28",
                "departure_date": "2020-10-29",
                "room_no": "1010",
                "room_type": "Premier",
                "adults": 2,
                "children": 0,
                "check_out_status": 500,
                "item_total_amount": 3099.5,
                "tax_amount": 282.28,
                "grand_total": 3382.78,
                "items": [
                    {
                        "date": "2020-10-28",
                        "item_name": "Test Item X",
                        "amount": 600.0
                    },
                    {
                        "date": "2020-10-28",
                        "item_name": "Test Item Y",
                        "amount": 4000.0
                    },
                    {
                        "date": "2020-10-29",
                        "item_name": "Test Item Z",
                        "amount": 99.5
                    }
                ]
            }
        ],
        "total_amount": 4582.77,
        "overall_status": True
    }
}

check_out_bill_1 = {
    "status_code": 500,
    "data": {
        "reservation_info": [
            {
                "reservation_no": "8125B",
                "first_name": "YS",
                "last_name": "Test",
                "arrival_date": "2020-10-28",
                "departure_date": "2020-10-29",
                "room_no": "1010",
                "room_type": "Premier",
                "adults": 2,
                "children": 0,
                "check_out_status": 500,
                "item_total_amount": 1099.5,
                "tax_amount": 100.49,
                "grand_total": 1199.99,
                "items": [
                    {
                        "date": "2020-10-28",
                        "item_name": "Item X",
                        "amount": 600.0
                    },
                    {
                        "date": "2020-10-28",
                        "item_name": "Item Y",
                        "amount": 400.0
                    },
                    {
                        "date": "2020-10-28",
                        "item_name": "Item Z",
                        "amount": 99.5
                    }
                ]
            },
        ],
        "total_amount": 1199.99,
        "overall_status": False
    }
}

check_out_bill_2 = {
    "status_code": 500,
    "data": {
        "reservation_info": [
            {
                "reservation_no": "4FM1T",
                "first_name": "Shae",
                "last_name": "Test",
                "arrival_date": "2020-10-28",
                "departure_date": "2020-10-29",
                "room_no": "1010",
                "room_type": "Premier",
                "adults": 2,
                "children": 0,
                "check_out_status": 500,
                "item_total_amount": 3099.5,
                "tax_amount": 282.28,
                "grand_total": 3382.78,
                "items": [
                    {
                        "date": "2020-10-28",
                        "item_name": "Test Item X",
                        "amount": 600.0
                    },
                    {
                        "date": "2020-10-28",
                        "item_name": "Test Item Y",
                        "amount": 4000.0
                    },
                    {
                        "date": "2020-10-29",
                        "item_name": "Test Item Z",
                        "amount": 99.5
                    }
                ]
            }
        ],
        "total_amount": 3382.78,
        "overall_status": True
    }
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
    elif reservations_no == ['8125B']:
        return check_out_bill_1
    elif reservations_no == ['4FM1T']:
        return check_out_bill_2
    else:
        return check_out_bill_3
