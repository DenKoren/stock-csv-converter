import csv
from . import converters
from datetime import datetime


class TimeRow:
    def __init__(self, dt, o, h, l, c, v):
        """
        @param datetime dt:
        @param o:
        @param h:
        @param l:
        @param c:
        @param v:
        """
        self.dt = dt
        self.open = float(o)
        self.high = float(h)
        self.low = float(l)
        self.close = float(c)
        self.volume = int(v)

    @staticmethod
    def read_ninja_trader(infile):
        reader = csv.reader(infile, delimiter=";")

        for row in reader:
            dt = converters.parse_date_time(row[0])
            yield TimeRow(
                dt,
                float(row[1]),
                float(row[2]),
                float(row[3]),
                float(row[4]),
                int(row[5]),
            )

    @staticmethod
    def from_tick(tick, price):
        return TimeRow(
            tick.dt,
            price,
            price,
            price,
            price,
            tick.volume
        )

    @staticmethod
    def minutes_from_ticks(tick_rows):
        """
        @param TickRow tick_rows:
        """

        minute_row = None
        for tick in tick_rows:
            if minute_row is None:
                minute_row = TimeRow.from_tick(tick, tick.last)
                continue

            m_dt = minute_row.dt
            t_dt = tick.dt

            if m_dt.date() != t_dt.date() \
                    or m_dt.hour != t_dt.hour \
                    or m_dt.minute != t_dt.minute:
                yield minute_row
                minute_row = TimeRow.from_tick(tick, tick.last)
                continue

            minute_row.high = max(minute_row.high, tick.last)
            minute_row.low = min(minute_row.low, tick.last)
            minute_row.close = tick.last
            minute_row.volume = minute_row.volume + tick.volume

        if minute_row is not None:
            yield minute_row
