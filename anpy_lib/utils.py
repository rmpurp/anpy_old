import datetime

def date_to_tuple(date):
    return (date.year, date.month, date.day)

def time_to_tuple(time):
    return (time.hour, time.minute)

def get_most_recent_monday(date=None):
    if not date:
        date = datetime.date.today()
    return date - datetime.timedelta(days=date.weekday())
 
