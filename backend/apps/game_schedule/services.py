from datetime import datetime

def get_formatted_date(
    *,
    date: str
):
    year = date.year
    month = date.month
    day = date.day
    
    hour = date.hour + 8
    if hour < 0:
        hour += 24
        day -= 1
    
    if hour > 23:
        hour -= 24
        day += 1

    minute = date.minute

    date_format = datetime(year, month, day, hour, minute)
    return date_format