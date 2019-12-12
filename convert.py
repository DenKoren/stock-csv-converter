#!/usr/bin/env python

import csv
from collections import namedtuple
import sys

Row = namedtuple("Row", ["datetime", "open", "high", "low", "close", "volume"])
Date = namedtuple("Date", ["year", "month", "day"])
Time = namedtuple("Time", ["hour", "minute", "second"])
Data = namedtuple("Data", ["date", "time", "open", "high", "low", "close", "volume"])


def read_csv(infile):
    reader = csv.reader(infile, delimiter=";")

    for row in reader:
        yield Row(*row)


def parse_ninja_trader(row):
    (dateLine, timeLine) = row.datetime.split(" ")

    date = Date(
        dateLine[0:4],
        dateLine[4:6],
        dateLine[6:8],
    )

    time = Time(
        timeLine[0:2],
        timeLine[2:4],
        timeLine[4:6],
    )

    return Data(
        date,
        time,
        row.open,
        row.high,
        row.low,
        row.close,
        row.volume,
    )


def render_ts_lab(data):
    return '{month}/{day}/{year};{hour}:{minute};{open};{high};{low};{close};{volume};'.format(
        month=data.date.month,
        day=data.date.day,
        year=data.date.year,
        hour=data.time.hour,
        minute=data.time.minute,
        second=data.time.second,
        open=data.open,
        high=data.high,
        low=data.low,
        close=data.close,
        volume=data.volume
    )


def main():
    for row in read_csv(sys.stdin):
        data = parse_ninja_trader(row)
        print(render_ts_lab(data))


if __name__ == "__main__":
    main()
