# stock-csv-converter
Stock exchange data CSV converter

This script is designed to convert CSV data exported from one tranding platform to format acceptable for another platform.

Currently it supports only [NinjaTrader platform](https://ninjatrader.com/) as 'input' format and [TsLab](http://www.tslab.ru/) as output.

Converter works as regular *nix filter command:

```bash
cat "ninja-trader.csv" | ./convert.py > "ts-lab.csv"
```