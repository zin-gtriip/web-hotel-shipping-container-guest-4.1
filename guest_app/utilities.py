import datetime as dt
from datetime import datetime

def calculate_age(birthdate):
    """
    Calculate age based on passed date and date now
    """
    if not birthdate: return 0
    born = datetime.strptime(birthdate, '%d/%m/%Y')
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


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
