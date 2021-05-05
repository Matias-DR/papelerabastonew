from record import (
    Record, StockRecord, SaleRecord, BuyRecord
)
from PySimpleGUI import (
    Column
)
from constants import (
    JSON_STOCK_PATH, JSON_SALES_PATH, JSON_BUYS_PATH, CSV_SALES_PATH, CSV_BUYS_PATH, DATE, TIME,
    RECORDLIST_COLUMN_SIZE, RECORDLIST_COLUMN_PAD, SALELIST_COLUMN_SIZE, SALELIST_COLUMN_PAD,
    BUYSLIST_COLUMN_SIZE, BUYSLIST_COLUMN_PAD
)
from json import (
    load, dump
)
from csv import writer
from os import system as sys


class FileManager:
    @staticmethod
    def load(path: str):
        with open(path) as file:
            return load(file)

    @staticmethod
    def save_in_json(path: str, data):
        with open(path, 'w') as file:
            dump(data, file, indent=4)

    @staticmethod
    def save_in_csv(path: str, data: list, mode: str='a'):
        with open(path, mode, newline='') as f:
            wr = writer(f, delimiter=',', )
            for line in data:
                wr.writerow(line)


class RecordList(Column):
    """
    Superclase que define elementos predeterminados para toda lista de registros
    """
    def __init__(self, records: list, size: tuple, pad=tuple):
        super().__init__(layout=records,
                         size=size,
                         pad=pad,
                         scrollable=True,
                         vertical_scroll_only=True)

    def report(self):
        """
        :return: List[List[]]
        """
        return [
            rc[0].report() for rc in self.Rows
        ]

    def search(self, name: str):
        """
        Indica el índice del registro existente, -1 en caso de no existir\n
        :return: int
        """
        for i, rc in enumerate(self.Rows):
            if rc[0].get_name().upper() == name.upper():
                return i
        return -1

    def get_record(self, name: str):
        """
        Devuelve el registro si existe, o unvalor nulo si no existe\n
        :return: Record
        """
        try:
            return self.Rows[self.search(name)][0]
        except:
            return None

    def remove_checked_records(self):
        for rc in reversed(self.Rows):
            if rc[0].is_checked():
                self.Rows.remove(rc)

    def update_from_report(self, report: list):
        for i, rc in enumerate(self.Rows):
            rc[0].update_from_report(report[i])

    def sort_list_min_max(self, field: int):
        self.update_from_report(sorted(self.report(), key=lambda rc: rc[field]))

    def sort_list_max_min(self, field: int):
        self.update_from_report(sorted(self.report(), key=lambda rc: rc[field], reverse=True))

    def add_record(self, record: Record):
        row = [
            record
        ]
        self.Rows.append(row)

    def get_list_report(self):
        """
        :return: List[List[Fields]]
        """
        return [
            rc[0].get_report() for rc in self.Rows
        ]

    def get_list_control(self):
        """
        :return: Boolean
        """
        self.solve_error()
        for rc in self.Rows:
            error = rc[0].get_error_status()
            if error > -1:
                rc[0].indicate_error(error)
                return False
        return True

    def solve_error(self):
        for rc in self.Rows:
            rc[0].solve_error()


class StockList(RecordList):
    _instance = None

    @classmethod
    def instance(cls):
        if not StockList._instance:
            _instance = StockList()
        return _instance

    def __init__(self):
        super().__init__(records=FileManager.load(path=JSON_STOCK_PATH),
                         size=RECORDLIST_COLUMN_SIZE,
                         pad=RECORDLIST_COLUMN_PAD)

    def remove_empty_records(self):
        for rc in reversed(self.Rows):
            if rc[0].is_empty():
                self.Rows.remove(rc)

    def get_records_to_apply_percent(self):
        """
        :return: List[List[]]
        """
        return filter(lambda record: record[0].have_percent_to_apply(), self.Rows)

    def apply_percent_to_records(self):
        for rc in self.get_records_to_apply_percent():
            rc[0].apply_percent()

    def add_records(self, how_many_add: int):
        for _ in range(how_many_add):
            self.add_record(StockRecord())

    def add_record_from_buy(self, name: str, unit_price: float, stock: int):
        self.add_record(StockRecord(name=name, unit_price=unit_price, stock=stock))

    def update_records_from_buy(self, records: list):
        for rc in records:
            existent_record = self.get_record(rc[0])
            if existent_record:
                existent_record.update_from_buy(rc[1], rc[2])
            else:
                self.add_record_from_buy(rc[0], rc[1], [2])

    def update_records_from_sale(self, records: list):
        for rc in records:
            self.get_record(rc[0]).update_from_sale(rc[1])

    def get_checked_records(self):
        """
        :return: List[Record]
        """
        checked_records = []
        for rc in self.Rows:
            if rc[0].is_checked():
                checked_records.append(rc[0])
        return checked_records

    def collect_unit_price_records(self, names: list):
        """
        :return: List[List[Fields]]
        """
        records = []
        for name in names:
            record = self.get_record(name)
            if record:
                records.append({'name': name, 'unit_price': record.get_unit_price()})
        return records

    def save_in_json(self):
        FileManager.save_in_json(JSON_STOCK_PATH, self.get_list_report())

    def export(self, path: str):
        csv_report = [
            [
                'NOMBRE', 'PRECIO POR UNIDAD', 'STOCK'
            ]
        ]
        csv_report += self.get_list_report()
        FileManager.save_in_csv(path=path, data=csv_report, mode='w')


class CommerceList(RecordList):
    def __init__(self, path: str, size: tuple, pad: tuple):
        super().__init__(records=FileManager.load(path=path),
                         size=size,
                         pad=pad)

    def remove_all_records(self):
        self.Rows = []

    def get_csv_report(self):
        """
        :return: List[List[]]
        """
        csv_report = [
            [
                DATE(), TIME()
            ]
        ]
        for rc in self.Rows:
            csv_report += rc[0].get_csv_report()
        return csv_report


class SaleList(CommerceList):
    _instance = None

    @classmethod
    def instance(cls):
        if not StockList._instance:
            _instance = StockList()
        return _instance

    def __init__(self):
        super().__init__(path=JSON_SALES_PATH, size=SALELIST_COLUMN_SIZE, pad=SALELIST_COLUMN_PAD)

    def save_in_csv(self):
        FileManager.save_in_csv(path=CSV_SALES_PATH, data=self.get_csv_report())

    def save_in_json(self):
        FileManager.save_in_json(path=JSON_SALES_PATH, data=self.get_list_report())

    def get_sale_report(self):
        """
        :return: List[Fields]
        """
        sale_report = []
        for rc in self.Rows:
            sale_report.append(rc[0].get_name(), rc[0].get_amount())

    def sell(self):
        if self.get_list_control():
            self.save_in_csv()
            StockList.instance().update_records_from_sale(self.get_sale_report())
            self.remove_all_records()

    def export(self, path: str):
        sys(f'cp {CSV_SALES_PATH} {path}')

    def calculate_final_price(self):
        """
        :return: Float
        """
        final_price = 0
        for rc in self.Rows:
            final_price += rc[0].apply_final_price()
        return final_price
