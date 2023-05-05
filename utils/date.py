import datetime
import re


def arrivedate(date: str):
    try:
        d, m, y = re.split('\W', date)

        if len(d) == 1:
            d = "0" + d
        if len(m) == 1:
            m = "0" + m
        if len(y) != 4:
            y = "20" + y

        today = datetime.datetime.toordinal(datetime.datetime.now())
        date = datetime.datetime.toordinal(datetime.date(int(y), int(m), int(d)))

        if date < today:
            raise ValueError

    except:
        return False

    return d, m, y, date


def departdate(days: str, date: str):
    if days.isdigit() and int(days) > 0:
        depdate = int(date) + int(days)
        depdate = datetime.datetime.date(datetime.datetime.fromordinal(depdate))
        y, m, d = re.split('\W', str(depdate))
    else:
        return False

    return d, m, y

