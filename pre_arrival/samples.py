from django.utils.translation   import gettext, gettext_lazy as _

pre_arrival_get_data = {
    "overall_status": 500,
    "data": [
        {
            "property": "Amara Sanctuary",
            "reservationNo": "1234",
            "otaNo": "123456",
            "reservationStatus": "reserved",
            "adults": "3",
            "children": "5",
            "arrivalDate": "2020-07-14",
            "departureDate": "2020-07-20",
            "eta": "10:00:00",
            "guestsId": [1, 2],
            "guestsList": [
                {
                    "guestID": "1",
                    "salutation": "Mr.",
                    "firstName": "Columbus",
                    "lastName": "Leonard",
                    "passportNo": "A12345X",
                    "nationality": "US",
                    "dob": "1980-12-31",
                    "email": "columbus@a.com",
                    "emailSubscription": "1",
                    "isMainGuest": '1'
                },
                {
                    "guestID": "2",
                    "salutation": "Ms.",
                    "firstName": "Jacquelin",
                    "lastName": "F.",
                    "passportNo": "A34236X",
                    "nationality": "US",
                    "dob": "1986-07-05",
                    "email": "jacquelin@a.com",
                    "emailSubscription": "0",
                    "isMainGuest": '0'
                }
            ],
            "roomNo": "736",
            "roomType": "Deluxe Room",
            "roomRate": "99.98999786376953",
            "roomStatus": "Ready",
            "paymentType": "Credit card",
            "paymentToken": "@\u0026@HF!",
            "billsId": [1],
            "comments": "Very good service and friendly front desk!",
        },
        {
            "property": "Amara Sanctuary",
            "reservationNo": "3333",
            "otaNo": "123456",
            "reservationStatus": "reserved",
            "adults": "3",
            "children": "5",
            "arrivalDate": "2020-07-14",
            "departureDate": "2020-07-20",
            "eta": "10:00:00",
            "guestsId": [5, 6, 7],
            "guestsList": [
                {
                    "guestID": "5",
                    "salutation": "Mr.",
                    "firstName": "John",
                    "lastName": "Leonard",
                    "passportNo": "A85667X",
                    "nationality": "US",
                    "dob": "2010-12-02",
                    "email": "-",
                    "emailSubscription": "0",
                    "isMainGuest": '0'
                },
                {
                    "guestID": "6",
                    "salutation": "Mr.",
                    "firstName": "Alex",
                    "lastName": "Leonard",
                    "passportNo": "A74574X",
                    "nationality": "US",
                    "dob": "2000-07-04",
                    "email": "alexleo@a.com",
                    "emailSubscription": "0",
                    "isMainGuest": '1'
                },
                {
                    "guestID": "7",
                    "salutation": "Ms.",
                    "firstName": "Jane",
                    "lastName": "Leonard",
                    "passportNo": "A56345X",
                    "nationality": "US",
                    "dob": "2002-03-05",
                    "email": "janeleo@a.com",
                    "emailSubscription": "0",
                    "isMainGuest": '0'
                }
            ],
            "roomNo": "737",
            "roomType": "Premier Room",
            "roomRate": "99.98999786376953",
            "roomStatus": "Ready",
            "paymentType": "Credit card",
            "paymentToken": "@\u0026@HF!",
            "billsId": [3],
            "comments": "Very good service and friendly front desk!"
        },
    ]
}

def get_data(post_data):
    return pre_arrival_get_data


pre_arrival_post_data = {
    'status': 'success',
    'data': [
        {
            "property": "Amara Sanctuary",
            "reservationNo": "1234",
            "otaNo": "123456",
            "reservationStatus": "reserved",
            "adults": "3",
            "children": "5",
            "arrivalDate": "2020-07-14",
            "departureDate": "2020-07-20",
            "eta": "10:00:00",
            "guestsId": [1, 2],
            "guestsList": [
                {
                    "guestID": "1",
                    "salutation": "Mr.",
                    "firstName": "Columbus",
                    "lastName": "Leonard",
                    "passportNo": "A12345X",
                    "nationality": "US",
                    "dob": "1980-12-31",
                    "email": "columbus@a.com",
                    "emailSubscription": "1",
                    "isMainGuest": 1
                },
                {
                    "guestID": "2",
                    "salutation": "Ms.",
                    "firstName": "Jacquelin",
                    "lastName": "F.",
                    "passportNo": "A34236X",
                    "nationality": "US",
                    "dob": "1986-07-05",
                    "email": "jacquelin@a.com",
                    "emailSubscription": "0",
                    "isMainGuest": 0
                }
            ],
            "roomNo": "736",
            "roomType": "Deluxe Room",
            "roomRate": "99.98999786376953",
            "roomStatus": "Ready",
            "paymentType": "Credit card",
            "paymentToken": "@\u0026@HF!",
            "billsId": [1],
            "comments": "Very good service and friendly front desk!",
        },
    ],
}

def send_data(post_data):
    return pre_arrival_post_data
