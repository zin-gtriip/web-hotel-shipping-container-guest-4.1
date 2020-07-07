import datetime as dt
from datetime import datetime

def calculate_age(date):
    """
    Calculate age based on passed date and date now
    Passed date format needs to be `yyyy-mm-dd`
    """
    if not date: return 0
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
    except:
        return 0
    today = datetime.today()
    return today.year - date.year - ((today.month, today.day) < (date.month, date.day))


def generate_time_arrival():
    """
    Generate array of time with interval 30 sec
    """
    result = []
    loop = datetime.strptime('00:00', '%H:%M')
    end = datetime.strptime('23:59', '%H:%M')
    while(loop < end):
        result.append((datetime.strftime(loop, '%H:%M'), datetime.strftime(loop, '%H:%M')))
        loop += dt.timedelta(minutes=30)
    return result

def format_ocr_date(date):
    """
    Format date from OCR response `dd-mm-yyyy` to `yyyy-mm-dd`
    """
    if not date: return
    return datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
