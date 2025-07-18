from datetime import datetime

def get_date_range_from_week(year_week_str: str) -> tuple[datetime, datetime]:
    year, week = year_week_str.split('-W')
    year, week = int(year), int(week)
    first_day = datetime.fromisocalendar(year, week, 1)
    last_day = datetime.fromisocalendar(year, week, 7)
    return first_day, last_day
