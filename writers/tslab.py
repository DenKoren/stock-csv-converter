# vim: set fileencoding=utf-8 :

from rows import TimeRow
from rows import TickRow
import csv

# Список полей поддерживаемых TsLab:
#
#     <TICKER> - Наименование инструмента
#     <PER> - Период
#     <DATE> - Дата
#     <TIME> - Время
#     <OPEN> - Цена открытия свечи (только бары)
#     <LOW> - Цена минимума свечи (только бары)
#     <HIGH> - Цена максимума свечи (только бары)
#     <CLOSE> - Цена закрытия свечи (только бары)
#     <VOL> - объем бара(или сделки)
#     <OI> или <INTEREST> - Открытый интерес
#     <LAST> - Цена сделки (используется для тиковых данных)
#     <MSEC> - миллисекунды
#     <TRADENO> или <ID>  -номер сделки (для тиковых)
#     <LAST> - последнее значение(для тиковых)
#     <OPER> - направление сделки (для тиковых)
#     <ASK> - цена лучшего предложения продажи в очереди заявок(на момент закрытия бара, сделки)
#     <ASKQTY1> - объем лучшего предложения
#     <BID> - цена лучшего спроса
#     <BIDQTY1> - объем лучшего спроса
#     <STEPPRICE> - шаг цены
#
# Примеры вариантов:
#
#     1. Период одна минута
#         <TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
#         NYMEX.PL,1,20140801,000000,1462.9,1463.4,1462.9,1462.9,16
#         NYMEX.PL,1,20140801,000200,1463.6,1463.8,1462.9,1462.9,19
#         NYMEX.PL,1,20140801,000300,1463.8,1463.8,1463.8,1463.8,1
#         NYMEX.PL,1,20140801,000600,1463.2,1463.2,1462.70,1462.9,19
#
#     2. Период 1 тик с номером сделки
#         <DATE>,<TIME>,<LAST>,<VOL>,<ID>
#         20160713,100000,94150,2,1538194180
#         20160713,100000,94120,1,1538194181
#         20160713,100000,94100,1,1538194182
#         20160713,100000,94100,2,1538194183
#         20160713,100000,94100,1,1538194184
#
#     3. Период 1 тик с направлением сделки и данными по лучшим спросу и предложению, с открытым интересом
#         <DATE>,<TIME>,<MSEC>,<TRADENO>,<LAST>,<VOL>,<OPER>,<ASK1>,<ASKQTY1>,<BID1>,<BIDQTY1>,<INTEREST>,<STEPPRICE>
#         20190108,100000,000,2206980738,1.1473,1,B,1.1515,1951,1.1462,4187,103604,6.78181
#         20190108,100000,000,2206980739,1.1478,1,B,1.1515,1951,1.1462,4187,103604,6.78181
#         20190108,100000,000,2206980740,1.1478,1,B,1.1515,1951,1.1462,4187,103604,6.78181
#         20190108,100000,000,2206980741,1.1483,4,B,1.1515,1951,1.1462,4187,103604,6.78181


class MinuteWriter:
    out: csv.DictWriter

    def __init__(self, out):
        """
        :param file out:
        """
        writer = csv.DictWriter(
            out,
            fieldnames=[
                "<TICKER>", "<DATE>", "<TIME>", "<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>", "<VOL>"
            ],
            delimiter=","
        )
        self.out = writer

    @staticmethod
    def format(minute):
        """
        @param TimeRow minute:
        """
        return {
            "<TICKER>": minute.ticker,
            "<DATE>": minute.dt.strftime("%m/%d/%Y"),
            "<TIME>": minute.dt.strftime("%H:%M"),
            "<OPEN>": minute.open,
            "<LOW>": minute.low,
            "<HIGH>": minute.high,
            "<CLOSE>": minute.close,
            "<VOL>": minute.volume
        }

    def write(self, row):
        """
        @param TimeRow row:
        """
        return self.out.writerow(MinuteWriter.format(row))


class TickWriter:
    out: csv.DictWriter
    header_saved: bool

    def __init__(self, out):
        writer = csv.DictWriter(
            out,
            fieldnames=["<TICKER>", "<DATE>", "<TIME>", "<MSEC>", "<LAST>", "<BID>", "<ASK>", "<VOL>"],
            delimiter=","
        )
        self.out = writer
        self.header_saved = False

    @staticmethod
    def format(tick):
        """
        :param TickRow tick:
        :return:
        """
        return {
            "<TICKER>": tick.ticker,
            "<DATE>": tick.dt.strftime("%Y%m%d"),
            "<TIME>": tick.dt.strftime("%H%M%S"),
            "<MSEC>": tick.dt.strftime("%f")[:3],
            "<LAST>": tick.last,
            "<BID>": tick.bid,
            "<ASK>": tick.ask,
            "<VOL>": tick.volume,
        }

    def write(self, row):
        """
        :param TickRow row:
        :return:
        """

        if not self.header_saved:
            self.out.writeheader()
            self.header_saved = True

        return self.out.writerow(TickWriter.format(row))
