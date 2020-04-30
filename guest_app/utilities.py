from datetime import datetime

def calculate_age(birthdate):
    if not birthdate: return 0
    born = datetime.strptime(birthdate, '%d/%m/%Y')
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))