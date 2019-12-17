#!/usr/bin/env python

import csv
import sys

import rows
import formatters


def main():
    infile = sys.stdin
    if len(sys.argv) > 1:
        infile = open(sys.argv[1], "r")

    writer = csv.writer(sys.stdout, delimiter=";")
    ticks = rows.TickRow.read_ninja_trader(infile)
    for minute_row in rows.TimeRow.minutes_from_ticks(ticks):
        writer.writerow(formatters.tslab(minute_row))


if __name__ == "__main__":
    main()
