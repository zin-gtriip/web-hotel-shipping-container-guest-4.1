import datetime, os
from datetime                   import datetime as dt
from django.utils               import timezone
from django.utils.translation   import gettext, gettext_lazy as _
from django.conf                import settings
from django.template.loader     import render_to_string


def calculate_age(date):
    """
    Calculate age based on passed date and date now
    Passed date format needs to be `yyyy-mm-dd`
    """
    if not date or not isinstance(date, datetime.date): return 0
    today = timezone.now()
    return today.year - date.year - ((today.month, today.day) < (date.month, date.day))


def parse_ocr_date(date):
    """
    Parse date from OCR response `dd-mm-yyyy` to date object
    """
    if not date: return
    return dt.strptime(date, '%d/%m/%Y')


def format_display_date(date):
    """
    Convert string to date format `Mon, 01/01/20`
    """
    try:
        date = dt.strptime(date, '%Y-%m-%d')
    except:
        date = None
    if not date: return
    return date.strftime('%a, %d/%m/%y')


def generate_arrival_time():
    """
    Generate array of time with interval 30 sec
    """
    result = []
    loop = dt.strptime('00:00', '%H:%M')
    end = dt.strptime('23:59', '%H:%M')
    while(loop < end):
        result.append((dt.strftime(loop, '%H:%M'), dt.strftime(loop, '%H:%M')))
        loop += datetime.timedelta(minutes=30)
    return result


def parse_arrival_time(time):
    """
    Convert string to time format `00:00`
    """
    try:
        time = dt.strptime(time, '%H:%M:%S')
    except:
        time = dt.strptime('14:00', '%H:%M')
    return time.strftime('%H:%M')


def prepare_email(context):
    context['formattedArrivalDate'] = format_display_date(context.get('arrivalDate', ''))
    context['formattedDepartureDate'] = format_display_date(context.get('departureDate', ''))
    main_guest = next(guest for guest in context.get('guestsList', []) if guest.get('isMainGuest', False))
    context['mainGuestFirstName'] = main_guest.get('firstName', '')
    context['mainGuestLastName'] = main_guest.get('lastName', '')
    room = next((temp for temp in settings.REGISTRATION_ROOM_TYPES if temp['room_type'] == context['roomType']), {})
    context['roomName'] = room.get('room_name', '')
    context['roomImage'] = settings.HOST_URL + room.get('room_image', '')
    context['hotelName'] = settings.HOTEL_NAME
    context['staticURL'] = settings.HOST_URL + settings.STATIC_IMAGE_URL
    context['iOSURL'] = settings.APP_IOS_URL
    context['androidURL'] = settings.APP_ANDROID_URL
    email = {}
    template = settings.REGISTRATION_COMPLETE_EMAIL or os.path.join(settings.BASE_DIR, 'registration', 'templates', 'registration', 'email', 'complete.html')
    email['title'] = _('Registration Complete - %(hotel_name)s - Reservation #%(pms_no)s') % {'hotel_name': settings.HOTEL_NAME, 'pms_no': context.get('pmsNo', '')}
    email['html'] = render_to_string(template, context)
    return email
