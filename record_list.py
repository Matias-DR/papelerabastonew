from record import (
    Record, StockRecord, SaleRecord, BuyRecord
)
from PySimpleGUI import (
    theme, Window, Column, Button
)
from constants import (
    JSON_STOCK_PATH, JSON_SALES_PATH, JSON_BUYS_PATH, CSV_SALES_PATH, CSV_BUYS_PATH, JSON_PATHS,
    RECORDLIST_COLUMN_SIZE, RECORDLIST_COLUMN_PAD, SALELIST_COLUMN_SIZE, SALELIST_COLUMN_PAD,
    BUYLIST_COLUMN_SIZE, BUYLIST_COLUMN_PAD, BUTTON_BORDER_WIDTH, DATE, TIME, CSV_SALES_HEADER,
    CSV_BUYS_HEADER
)
import constants as ct
from json import (
    load, dump
)
from csv import writer
import os
from multiprocessing import Process
from sys import platform


class FileManager:
    @staticmethod
    def restart(location=(20, 20)):
        if platform == 'win32':
            os.system('python record_list.py')
        else:
            os.system(f'python3 record_list.py {location[0]} {location[1]}')

    @staticmethod
    def create_json_files():
        for path in JSON_PATHS:
            with open(path, 'w') as file:
                dump([], file)

    @staticmethod
    def create_csv_files():
        FileManager.save_in_csv(path=CSV_SALES_PATH,
                                data=CSV_SALES_HEADER,
                                mode='w')
        FileManager.save_in_csv(path=CSV_BUYS_PATH,
                                data=CSV_BUYS_HEADER,
                                mode='w')

    @staticmethod
    def db_control():
        if not os.path.isdir('./db'):
            os.mkdir('./db')
            FileManager.create_json_files()
            FileManager.create_csv_files()

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
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls.new()
        return cls._instance

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

    def get_list_report(self):
        """
        :return: List[List[Fields]]
        """
        return [
            rc[0].get_report() for rc in self.Rows
        ]

    def get_checked_records(self):
        """
        :return: List[Record]
        """
        checked_records = []
        for rc in self.Rows:
            if rc[0].is_checked():
                checked_records.append(rc[0])
        return checked_records

    def have_checked_records(self):
        """
        :return: Boolean
        """
        for rc in self.Rows:
            if rc[0].is_checked():
                return True
        return False

    def get_list_control_status(self):
        """
        Indica el error dentro de los registros seleccionados\n
        :return: Boolean
        """
        if self.have_checked_records():
            self.solve_issues()
            for rc in self.get_checked_records():
                error = rc.get_error_status()
                if error > -1:
                    rc.indicate_issue(error)
                    return False
            return True
        return False

    def solve_issues(self):
        for rc in self.Rows:
            rc[0].solve_issue()


class StockList(RecordList):
    @classmethod
    def new(cls):
        records = [
            [
                StockRecord(name, unit_price, stock, percent, check)
            ] for name, unit_price, stock, percent, check in FileManager.load(path=JSON_STOCK_PATH)
        ]
        return cls(records)

    def __init__(self, records: list):
        super().__init__(records=records,
                         size=RECORDLIST_COLUMN_SIZE,
                         pad=RECORDLIST_COLUMN_PAD)

    def stock_control(self):
        self.solve_issues()
        for rc in self.Rows:
            if not rc[0].have_stock():
                rc[0].indicate_issue(index=2, color='Orange')

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
        records = FileManager.load(path=JSON_STOCK_PATH)
        for _ in range(how_many_add):
            records.append(StockRecord.get_empty_report())
        FileManager.save_in_json(path=JSON_STOCK_PATH, data=records)

    # REGACTOR
    def add_record_from_buy(self, name: str, unit_price: float, stock: int):
        pass
        # self.add_record(StockRecord(name=name, unit_price=unit_price, stock=stock))

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

    def collect_unit_prices_from_records(self, names: list):
        """
        :return: List[List[Fields]]
        """
        records = []
        for name in names:
            rc = self.get_record(name)
            if rc:
                _rc = [
                    name, rc.get_unit_price()
                ]
                records.append(_rc)
        return records

    def save_in_json(self):
        FileManager.save_in_json(JSON_STOCK_PATH, self.get_list_report())

    def export(self, path: str):
        csv_report = [
            [
                'DÍA', 'HORA', 'NOMBRE', 'PRECIO POR UNIDAD', 'STOCK'
            ]
        ]
        csv_report += self.get_list_report()
        FileManager.save_in_csv(path=path, data=csv_report, mode='w')

    def get_sale_control_status(self):
        """
        :return: Boolean
        """
        if self.have_checked_records():
            self.solve_issues()
            for rc in self.get_checked_records():
                if not rc.get_sale_control_status():
                    return False
            return True

    def sell_records(self):
        """
        :return: Boolean
        """
        if self.get_sale_control_status():
            report = [
                rc.get_sale_report() for rc in self.get_checked_records()
            ]
            SaleList.instance().add_records(report)
            return True
        return False


class CommerceList(RecordList):
    def __init__(self, records: list, size: tuple, pad: tuple):
        super().__init__(records=records,
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

    def calculate_final_price(self):
        """
        :return: Float
        """
        final_price = 0
        for rc in self.Rows:
            final_price += rc[0].apply_final_price()
        return final_price

    def get_commerce_report(self):
        """
        :return: List[Fields]
        """
        buy_report = []
        for rc in self.Rows:
            buy_report.append(rc[0].get_name(), rc[0].get_amount())


class SaleList(CommerceList):
    @classmethod
    def new(cls):
        records = [
            [
                SaleRecord(name, unit_price, stock, amount,
                           final_price, percent, check)
            ] for name, unit_price, stock, amount,
                  final_price, percent, check in FileManager.load(path=JSON_SALES_PATH)
        ]
        return cls(records)

    def __init__(self, records: list):
        super().__init__(records=records,
                         size=SALELIST_COLUMN_SIZE,
                         pad=SALELIST_COLUMN_PAD)

    def save_in_csv(self):
        FileManager.save_in_csv(path=CSV_SALES_PATH, data=self.get_csv_report())

    def save_in_json(self):
        FileManager.save_in_json(path=JSON_SALES_PATH, data=self.get_list_report())

    def sell(self):
        if self.get_list_control_status():
            self.save_in_csv()
            StockList.instance().update_records_from_sale(self.get_commerce_report())
            self.remove_all_records()

    def export(self, path: str):
        os.system(f'cp {CSV_SALES_PATH} {path}')

    def add_records(self, records: list):
        actual_records = self.get_list_report()
        name_records = [
            rc[0] for rc in actual_records
        ]
        for rc in records:
            try:
                index = name_records.index(rc[0])
                actual_record = actual_records[index]
                actual_record[1] = rc[1]
                actual_record[2] = rc[2]
            except:
                actual_records.append(rc)
        FileManager.save_in_json(path=JSON_SALES_PATH, data=actual_records)


class BuyList(CommerceList):
    @classmethod
    def new(cls):
        records = [
            [
                BuyRecord(name, unit_price, stock, amount,
                           final_price, supplier, percent, check)
            ] for name, unit_price, stock, amount,
                  final_price, supplier, percent, check in FileManager.load(path=JSON_BUYS_PATH)
        ]
        return cls(records)

    def __init__(self, records: list):
        super().__init__(records=records,
                         size=BUYLIST_COLUMN_SIZE,
                         pad=BUYLIST_COLUMN_PAD)

    def save_in_csv(self):
        FileManager.save_in_csv(path=CSV_BUYS_PATH, data=self.get_csv_report())

    def save_in_json(self):
        FileManager.save_in_json(path=JSON_BUYS_PATH, data=self.get_list_report())

    def buy(self):
        if self.get_list_control_status():
            self.save_in_csv()
            StockList.instance().update_records_from_buy(self.get_commerce_report())
            self.remove_all_records()

    def export(self, path: str):
        os.system(f'cp {CSV_BUYS_PATH} {path}')

    def get_record_names(self):
        """
        :return: List[String]
        """
        names = []
        for rc in self.Rows:
            names.append(rc[0].get_name())
        return names

    def collect_unit_prices(self):
        for rc in StockList.instance().collect_unit_prices_from_records(self.get_record_names()):
            self.get_record(rc[0]).update_unit_price(rc[1])

    def add_records(self, how_many_add: int):
        records = FileManager.load(path=JSON_BUYS_PATH)
        for _ in range(how_many_add):
            records.append(BuyRecord.get_empty_report())
        FileManager.save_in_json(path=JSON_BUYS_PATH, data=records)


class Test:
    def __init__(self):
        FileManager.db_control()
        layout = [
            [
                Button(button_text='test_add_records', border_width=BUTTON_BORDER_WIDTH),
                Button(button_text='test_sell_records', border_width=BUTTON_BORDER_WIDTH),
                Button(button_text='test_stock_control', border_width=BUTTON_BORDER_WIDTH),
            ], [
                StockList.instance(),
                SaleList.instance(),
                BuyList.instance()
            ]
        ]
        self.win = Window(title='test', layout=layout,
                          enable_close_attempted_event=True)
        self.lt = layout[-1]
        self.run()

    def save(self):
        for lt in self.lt:
            lt.save_in_json()

    def close(self, timeout=0):
        self.save()
        self.win.read(timeout=timeout, close=True)
        exit()

    def restart(self):
        Process(target=FileManager.restart, args=(self.win.current_location(), )).start()
        self.close(1000)

    def test_stock_control(self):
        self.lt[0].stock_control()

    def test_sell_records(self):
        if self.lt[0].sell_records():
            self.restart()

    def test_add_records(self):
        self.lt[0].add_records(2)
        self.lt[2].add_records(2)
        self.restart()

    def test_rows(self):
        print()
        print('TEST_STOCK_ROWS')
        print(self.lt[0].Rows)
        print()
        print('TEST_SALES_ROWS')
        print(self.lt[1].Rows)
        print()
        print('TEST_BUYS_ROWS')
        print(self.lt[2].Rows)
        print()

    def run(self):
        self.test_rows()
        while True:
            e, _ = self.win.read()
            if e == '-WINDOW CLOSE ATTEMPTED-':
                self.close()
                break
            getattr(self, e)()

if __name__ == '__main__':
    theme('PapelerAbasto')
    Test()
