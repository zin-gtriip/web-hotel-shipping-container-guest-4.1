check_out_data = {
    'overall_status': 500,
    'data': [
        {
            'reservation_no': '1111',
            'first_name': 'Alex',
            'last_name': 'Columbus',
            'item_total_amount': 134.04,
            'tax_amount': 13.43,
            'grand_total': 147.47,
            'status': 'checkout_enabled',
            'items': [
                {
                    'date': '2020-09-09',
                    'item_name': 'food',
                    'amount': 13.7,
                    'ref_no': ''
                },
                {
                    'date': '2020-09-09',
                    'item_name': 'food',
                    'amount': 10.0
                },
                {
                    'date': '2020-09-09',
                    'item_name': 'special',
                    'amount': 100.0
                },
                {
                    'date': '2020-09-09',
                    'item_name': 'special-special',
                    'amount': 100.0
                },
                {
                    'date': '2020-09-09',
                    'item_name': 'food and drinks',
                    'amount': 110.34
                }
            ]
        },
        {
            "reservation_no": "3333",
            "first_name": "Notalex",
            "last_name": "Columbus",
            "item_total_amount": 56.5,
            "tax_amount": 5.7,
            "grand_total": 62.2,
            "status": ["checkout_enabled", "checkout_disabled"],
            "items": [
                {
                    "date": "2020-09-09",
                    "item_name": "food",
                    "amount": 36.5
                },
                {
                    "date": "2020-09-09",
                    "item_name": "snacks",
                    "amount": 20.0
                }
            ]
        }
    ]
}
