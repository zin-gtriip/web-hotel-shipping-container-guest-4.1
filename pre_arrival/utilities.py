import datetime
from datetime       import datetime as dt
from django.utils   import timezone

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
        time = None
    if not time: return
    return time.strftime('%H:%M')
