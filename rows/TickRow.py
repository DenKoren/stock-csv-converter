import csv
from . import converters


class TickRow:
    def __init__(self, dt, last, bid, ask, volume):
        self.dt = dt
        self.last = last
        self.bid = bid
        self.ask = ask
        self.volume = volume

    @staticmethod
    def read_ninja_trader(infile):
        reader = csv.reader(infile, delimiter=";")

        for row in reader:
            dt = converters.parse_date_time(row[0])
            yield TickRow(
                dt,
                float(row[1]),
                float(row[2]),
                float(row[3]),
                int(row[4]),
            )
