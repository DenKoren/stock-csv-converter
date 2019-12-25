import csv
from . import converters
from datetime import datetime


class TickRow:
    def __init__(self, dt, last, bid, ask, volume, ticker=None):
        self.dt = dt
        self.last = last
        self.bid = bid
        self.ask = ask
        self.volume = volume

        self.ticker = ticker

    @staticmethod
    def read_ninja_trader(infile, ticker=None):
        """
        :param file infile:
        :param str ticker:
        :return:
        """
        reader = csv.reader(infile, delimiter=";")

        for row in reader:
            dt = converters.parse_date_time(row[0])
            yield TickRow(
                dt,
                float(row[1]),
                float(row[2]),
                float(row[3]),
                int(row[4]),
                ticker=ticker,
            )

    @property
    def to_time_last(self):
        """
        :return:
        """
        return TimeRow(
            self.dt,
            self.last,
            self.last,
            self.last,
            self.last,
            self.volume,
            ticker=self.ticker,
        )

    def to_time_ask(self):
        """
        :return:
        """
        return TimeRow(
            self.dt,
            self.ask,
            self.ask,
            self.ask,
            self.ask,
            self.volume,
            ticker=self.ticker,
        )

    def to_time_bid(self):
        """
        :return:
        """
        return TimeRow(
            self.dt,
            self.bid,
            self.bid,
            self.bid,
            self.bid,
            self.volume,
            ticker=self.ticker,
        )


class TimeRow:
    def __init__(self, dt, o, h, l, c, v, ticker=None):
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
        self.ticker = ticker

    @staticmethod
    def read_ninja_trader(infile, ticker=None):
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
                ticker=ticker,
            )

    @staticmethod
    def single_price(dt, price, volume, ticker):
        """
        :param datetime dt:
        :param float price:
        :param int volume:
        :param str ticker:
        :return:
        """
        return TimeRow(
            dt=dt,
            o=price,
            h=price,
            l=price,
            c=price,
            v=volume,
            ticker=ticker
        )

    @staticmethod
    def minutes_from_ticks(tick_rows):
        """
        @param list of TickRow tick_rows:
        """

        minute_row = None
        for tick in tick_rows:
            if minute_row is None:
                minute_row = tick.to_time_last
                continue

            m_dt = minute_row.dt
            t_dt = tick.dt

            if m_dt.date() != t_dt.date() \
                    or m_dt.hour != t_dt.hour \
                    or m_dt.minute != t_dt.minute:
                yield minute_row
                minute_row = tick.to_time_last
                continue

            minute_row.high = max(minute_row.high, tick.last)
            minute_row.low = min(minute_row.low, tick.last)
            minute_row.close = tick.last
            minute_row.volume = minute_row.volume + tick.volume

        if minute_row is not None:
            yield minute_row
