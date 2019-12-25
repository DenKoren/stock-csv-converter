#!/usr/bin/env python3

import sys

import rows
import writers.tslab as TsLabWriters


def main():
    infile = sys.stdin
    if len(sys.argv) > 1:
        infile = open(sys.argv[1], "r")

    ticker=None
    if len(sys.argv) > 2:
        ticker = sys.argv[2]

    ticks = rows.TickRow.read_ninja_trader(infile, ticker=ticker)

    # Convert to TsLab minutes format (csv)
    # writer = TsLabWriters.MinuteWriter(sys.stdout)
    # for minute_row in rows.TimeRow.minutes_from_ticks(ticks):
    #     writer.write(minute_row)

    # Convert to TsLab ticks format (txt)
    writer = TsLabWriters.TickWriter(sys.stdout)
    for tick in ticks:
        writer.write(tick)


if __name__ == "__main__":
    main()
