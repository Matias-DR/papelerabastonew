from record import Record, StockRecord, SaleRecord, BuyRecord
from PySimpleGUI import theme, Column, Button
import constants as cs
from json import load, dump
from csv import writer
import os
from sys import platform


class FileManager:
    @staticmethod
    def restart(location=(0, 0)):
        if platform == "win32":
            os.system("python gui.py")
        else:
            os.system(f"python3 gui.py {location[0]} {location[1]}")

    @staticmethod
    def create_json_files():
        for path in cs.JSON_PATHS:
            with open(path, "w") as file:
                dump([], file)

    @staticmethod
    def create_csv_files():
        FileManager.save_in_csv(
            path=cs.CSV_SALES_PATH, data=cs.CSV_SALES_HEADER, mode="w"
        )
        FileManager.save_in_csv(
            path=cs.CSV_BUYS_PATH, data=cs.CSV_BUYS_HEADER, mode="w"
        )

    @staticmethod
    def db_control():
        if not os.path.isdir("./db"):
            os.mkdir("./db")
            FileManager.create_json_files()
            FileManager.create_csv_files()

    @staticmethod
    def load(path: str):
        with open(path) as file:
            return load(file)

    @staticmethod
    def save_in_json(path: str, data):
        with open(path, "w") as file:
            dump(data, file, indent=4)

    @staticmethod
    def save_in_csv(path: str, data: list, mode: str = "a"):
        with open(path, mode, newline="") as f:
            wr = writer(
                f,
                delimiter=",",
            )
            for line in data:
                wr.writerow(line)


class RecordList(Column):
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls.new()
        return cls._instance

    def __init__(self, records: list, size: tuple, pad=tuple):
        super().__init__(
            layout=records,
            size=size,
            pad=pad,
            scrollable=True,
            vertical_scroll_only=True,
        )

    def __len__(self) -> int:
        return len(self.Rows)

    def _get_records(self) -> tuple[Record]:
        return tuple(map(lambda rc: rc[0], self.Rows))

    def _have_checked_records(self) -> bool:
        for rc in self._get_records():
            if rc.get_check():
                return True
        return False

    def _update_from_report(self, report: tuple):
        for i, rc in enumerate(self._get_records()):
            rc.upcs.date_from_report(report[i])

    def get_report(self) -> list[list]:
        return list(map(lambda rc: rc.get_report(), self._get_records()))

    def get_checked_records(self) -> tuple[Record]:
        return tuple(filter(lambda rc: rc.get_check(), self._get_records()))

    def get_record(self, name: str) -> Record:
        for rc in self._get_records():
            if rc.get_name().upper() == name.upper():
                return rc
        return None

    def get_record_names(self) -> list[str]:
        record_names = []
        for rc in self._get_records():
            name = rc.get_name()
            if name:
                record_names.append(name)
        return record_names

    def passes_control(self) -> bool:
        if self._have_checked_records():
            self.clear_issues()
            for rc in self.get_checked_records():
                if not rc.passes_control():
                    return False
            return True
        return False

    def sort_list_min_max(self, field: int):
        self._upcs.date_from_report(
            sorted(self.get_report(), key=lambda rc: rc[field])
        )

    def sort_list_max_min(self, field: int):
        self._upcs.date_from_report(
            sorted(self.get_report(), key=lambda rc: rc[field], reverse=True)
        )

    def uncheck_records(self):
        for rc in self.get_checked_records():
            rc.uncheck()

    def remove_checked_records(self) -> bool:
        if self._have_checked_records():
            for rc in reversed(self.Rows):
                if rc[0].get_check():
                    self.Rows.remove(rc)
            print(self.Rows)
            self.save_in_json()
            return True
        return False

    def clear_issues(self):
        for rc in self._get_records():
            rc.clear_issues()

    def check_all(self):
        for rc in self._get_records():
            rc.check()

    def save_in_json(self):
        FileManager.save_in_json(self.get_json_path(), self.get_report())


class StockAndBuyList:
    def have_empty_records(self) -> bool:
        for rc in reversed(self._get_records()):
            if rc.is_empty():
                return True
        return False

    def remove_empty_records(self):
        if self.have_empty_records():
            for rc in reversed(self.Rows):
                if rc[0].is_empty():
                    self.Rows.remove(rc)
            self.save_in_json()

    def add_records(self, how_many_add: int):
        report = self.get_report()
        for _ in range(how_many_add):
            report.append(self.get_class_record().get_empty_report())
        FileManager.save_in_json(path=self.get_json_path(), data=report)


class StockList(RecordList, StockAndBuyList):
    @classmethod
    def new(cls):
        records = [
            [StockRecord(name, unit_price, stock, percent, check)]
            for name, unit_price, stock, percent, check in
            FileManager.load(path=cs.JSON_STOCK_PATH)
        ]
        return cls(records)

    def __init__(self, records: list):
        RecordList.__init__(
            self,
            records=records,
            size=cs.RECORDLIST_COLUMN_SIZE,
            pad=cs.RECORDLIST_COLUMN_PAD,
        )
        StockAndBuyList.__init__(self)

    def get_json_path(self) -> str:
        return cs.JSON_STOCK_PATH

    def get_csv_report(self) -> list[list]:
        return cs.CSV_STOCK_HEADER + list(
            map(lambda rc: rc.get_csv_report(), self._get_records())
        )

    def get_class_record(self) -> Record:
        return StockRecord

    def passes_pre_sale_control(self) -> bool:
        if self._have_checked_records():
            self.clear_issues()
            for rc in self.get_checked_records():
                if not rc.passes_pre_sale_control():
                    return False
            return True
        return False

    def passes_pre_buy_control(self) -> bool:
        if self._have_checked_records():
            self.clear_issues()
            for rc in self.get_checked_records():
                if not rc.passes_pre_buy_control():
                    return False
            return True
        return False

    def passes_stock_control(self):
        self.clear_issues()
        for rc in self.get_checked_records():
            rc.passes_stock_control()

    def apply_percent_to_records(self):
        self.clear_issues()
        for rc in tuple(
            filter(
                lambda rc: rc.passes_apply_percent_control(),
                self._get_records()
            )
        ):
            rc.apply_percent()

    def add_records_from_buys_report(self, buys_report: list):
        FileManager.save_in_json(
            cs.JSON_STOCK_PATH,
            self.get_report() + buys_report
        )

    def update_record_from_buy_report(self, buy_report: list) -> bool:
        record = self.get_record(buy_report[0])
        if record:
            record.upcs.date_from_buy(buy_report[1], buy_report[2])
            return False
        return True

    def complete_buy_report(self, buys_report: list):
        for buy_report in buys_report:
            buy_report += [0, False]

    def receive_buys_report(self, buys_report: list):
        filtered_buys_report = list(
            filter(self.upcs.date_record_from_buy_report, buys_report)
        )
        if filtered_buys_report:
            self.complete_buy_report(filtered_buys_report)
            self.add_records_from_buys_report(filtered_buys_report)
        else:
            self.save_in_json()

    def update_record_from_sale_report(self, sale_report: list):
        self.get_record(sale_report[0]).upcs.date_from_sale(sale_report[1])

    def receive_sales_report(self, sales_report: list):
        for sale_report in sales_report:
            self.upcs.date_record_from_sale_report(sale_report)
        self.save_in_json()

    def export(self, path: str):
        FileManager.save_in_csv(path=path, data=self.get_csv_report(), mode="w")

    def get_pre_commerce_report(self) -> list[list]:
        return list(
            map(
                lambda rc: rc.get_pre_commerce_report(),
                self.get_checked_records()
            )
        )

    def pre_sell(self):
        self.save_in_json()
        if self.passes_pre_sale_control():
            SaleList.instance().pre_commerce_from_report(
                self.get_pre_commerce_report()
            )

    def pre_buy(self):
        self.save_in_json()
        if self.passes_pre_buy_control():
            BuyList.instance().pre_commerce_from_report(
                self.get_pre_commerce_report()
            )

    def secure_mode(self):
        StockRecord.change_secure_mode()
        for rc in self._get_records():
            rc.secure_mode()

    def have_record(self, name: str) -> bool:
        if self.get_record(name):
            return True
        return False

    def collect_unit_price_from_record_name(self, name: str) -> tuple:
        return (name, self.get_record(name).get_unit_price())

    def collect_unit_price_from_record_names(self, names: tuple) -> tuple:
        return tuple(
            map(
                self.collect_unit_price_from_record_name,
                list(set(self.get_record_names()).intersection(set(names)))
            )
        )

    def passes_buy_control(self, record_names: tuple) -> bool:
        self.clear_issues()
        for record_name in record_names:
            record = self.get_record(record_name)
            if record:
                if record.passes_control():
                    return True
                else:
                    return False
        return True

    def passes_sale_control(self, record_names: tuple) -> bool:
        self.clear_issues()
        for record_name in record_names:
            record = self.get_record(record_name)
            if record:
                if record.passes_control():
                    if not record.have_stock():
                        record.indicate_issue(2)
                        return False
                    return True
                else:
                    return False
        return True


class CommerceList(RecordList):
    def __init__(self, records: list, size: tuple, pad: tuple):
        super().__init__(records=records, size=size, pad=pad)

    def _remove_all_records(self):
        self.Rows = []

    def get_sale_report(self) -> list:
        return list(map(lambda rc: (rc.get_sale_report()), self._get_records()))

    def get_buy_report(self) -> list:
        return list(map(lambda rc: (rc.get_buy_report()), self._get_records()))

    def get_csv_report(self) -> list[list]:
        return cs.CSV_HEADER + list(
            map(lambda rc: rc.get_csv_report(), self._get_records())
        )

    def apply_final_price(self) -> float:
        return sum(
            tuple(map(lambda rc: rc.apply_final_price(), self._get_records()))
        )

    def save_in_csv(self):
        FileManager.save_in_csv(
            path=self.get_csv_path(), data=self.get_csv_report()
        )

    def export(self, path: str):
        if platform == 'win32':
            __import__('subprocess').call(
                f'C:\Windows\WinSxS\wow64_microsoft-windows-powershell-exe_31bf3856ad364e35_10.0.19041.546_none_5163f0069562aff6\powershell.exe cp {self.get_csv_path()} {path}',
                shell=True
            )
        else:
            os.system(f'cp {self.get_csv_path()} {path}')

    def update_existent_record(self, report: tuple) -> bool:
        existent_record = self.get_record(report[0])
        if existent_record:
            existent_record.upcs.date_from_report(report)
            return False
        return True

    def pre_commerce_from_report(self, report: tuple):
        filtered_report = list(filter(self.upcs.date_existent_record, report))
        if filtered_report:
            self.complete_pre_sell_report(filtered_report)
            FileManager.save_in_json(
                path=self.get_json_path(),
                data=filtered_report + self.get_report()
            )

    def passes_have_amount_control(self) -> bool:
        for rc in self.get_checked_records():
            if not rc.get_amount() > 0:
                rc.indicate_issue(3)
                return False
        return True

    def get_checked_record_names(self) -> tuple[str]:
        return tuple(map(lambda rc: rc.get_name(), self.get_checked_records()))


class SaleList(CommerceList):
    @classmethod
    def new(cls):
        records = [
            [
                SaleRecord(
                    name, unit_price, stock, amount, final_price, percent, check
                )
            ] for name, unit_price, stock, amount, final_price, percent, check
            in FileManager.load(path=cs.JSON_SALES_PATH)
        ]
        return cls(records)

    def __init__(self, records: list):
        super().__init__(
            records=records,
            size=cs.SALELIST_COLUMN_SIZE,
            pad=cs.SALELIST_COLUMN_PAD
        )

    def get_csv_path(self):
        return cs.CSV_SALES_PATH

    def get_json_path(self):
        return cs.JSON_SALES_PATH

    def get_sale_report(self) -> tuple[tuple]:
        return tuple(map(lambda rc: rc.get_sale_report(), self._get_records()))

    def upload_commerce_report(self):
        StockList.instance().receive_sales_report(self.get_sale_report())

    def records_existence_control(self) -> bool:
        for rc in self.get_checked_records():
            if not StockList.instance().have_record(rc.get_name()):
                rc.indicate_issue(0)
                return False
        return True

    def passes_control(self) -> bool:
        self.clear_issues()
        if super().passes_control():
            if self.records_existence_control():
                return True
        return False

    def complete_pre_sell_report(self, pre_sell_report: list):
        for report in pre_sell_report:
            report += [0, 0, 0, False]

    def sell_records(self):
        if self.passes_control():
            if self.passes_have_amount_control():
                if StockList.instance().passes_sale_control(
                    self.get_checked_record_names()
                ):
                    self.upload_commerce_report()
                    self.save_in_csv()
                    self.remove_checked_records()
                    self.save_in_json()


class BuyList(CommerceList, StockAndBuyList):
    @classmethod
    def new(cls):
        records = [
            [
                BuyRecord(
                    name,
                    unit_price,
                    stock,
                    amount,
                    final_price,
                    supplier,
                    percent,
                    check,
                )
            ] for name, unit_price, stock, amount, final_price, supplier,
            percent, check in FileManager.load(path=cs.JSON_BUYS_PATH)
        ]
        return cls(records)

    def __init__(self, records: list):
        CommerceList.__init__(
            self,
            records=records,
            size=cs.BUYLIST_COLUMN_SIZE,
            pad=cs.BUYLIST_COLUMN_PAD
        )
        StockAndBuyList.__init__(self)

    def get_buy_report(self) -> list[list]:
        return tuple(map(lambda rc: rc.get_buy_report(), self._get_records()))

    def get_class_record(self) -> Record:
        return BuyRecord

    def get_csv_path(self) -> str:
        return cs.CSV_BUYS_PATH

    def get_json_path(self) -> str:
        return cs.JSON_BUYS_PATH

    def upload_commerce_report(self):
        StockList.instance().receive_buys_report(self.get_buy_report())

    def collect_unit_prices(self):
        for rc in StockList.instance().collect_unit_price_from_record_names(
            self.get_record_names()
        ):
            self.get_record(rc[0]).upcs.date_unit_price(rc[1])

    def complete_pre_sell_report(self, pre_sell_report: list):
        for report in pre_sell_report:
            report += [0, 0, '', 0, False]

    def buy_records(self):
        if self.passes_control():
            if self.passes_have_amount_control():
                if StockList.instance().passes_buy_control(
                    self.get_checked_record_names()
                ):
                    self.upload_commerce_report()
                    self.save_in_csv()
                    self.remove_checked_records()
                    self.save_in_json()
