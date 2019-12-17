from datetime import datetime


def parse_date_time(dtstring):
    (dateLine, timeLine, microsecond) = dtstring.split(" ")

    return datetime(
        year=int(dateLine[0:4]),
        month=int(dateLine[4:6]),
        day=int(dateLine[6:8]),
        hour=int(timeLine[0:2]),
        minute=int(timeLine[2:4]),
        second=int(timeLine[4:6]),
        microsecond=int(microsecond[0:6])
    )
