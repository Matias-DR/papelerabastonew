from PySimpleGUI import (
    T, theme, Window, Column, Frame, Tab, TabGroup, Button, SaveAs, Input,
    Combo, Spin, Radio, Text, Checkbox
)
import constants as cs
from multiprocessing import Process
from json import (load, dump)
from csv import writer
import os
from sys import platform
from subprocess import call


# ------------------------------ #
#        generic_tools.py        #
# ------------------------------ #
class Config:
    def setattr_in_object_from_objects(in_object, *from_objects):
        for from_object in from_objects:
            for function in dir(from_object):
                if not function.startswith('_'):
                    setattr(in_object, function, getattr(from_object, function))


# ------------------------------ #
#         record_tools.py        #
# ------------------------------ #
class BaseRecordControl:
    def __init__(self, record_list):
        self._record_list = record_list

    def have_unit_price(self) -> bool:
        return self._record_list.get_unit_price() > 0

    def passes_base_control(self) -> bool:
        if self._record_list.get_name() == '':
            self._record_list.indicate_issue(0)
            return False
        try:
            error = 1
            self._record_list.get_unit_price()
            error = 2
            self._record_list.get_stock()
        except:
            self._record_list.indicate_issue(error)
            return False
        return True


# ------------------------------ #
#      record_list_tools.py      #
# ------------------------------ #
class FileManager:
    @staticmethod
    def restart(location=(0, 0)):
        if platform == "win32":
            os.system("python __init__.py")
        else:
            os.system(f"python3.9 __init__.py {location[0]} {location[1]}")

    def create_json_files():
        for path in cs.JSON_PATHS:
            with open(path, "w") as file:
                dump([], file)

    def create_csv_files():
        FileManager.save_in_csv(
            path=cs.CSV_SALES_PATH, data=cs.CSV_SALES_HEADER, mode="w"
        )
        FileManager.save_in_csv(
            path=cs.CSV_BUYS_PATH, data=cs.CSV_BUYS_HEADER, mode="w"
        )

    def create_theme_file():
        with open('./db/THEME', 'w') as file:
            file.write('PapelerAbasto')

    def db_control():
        if not os.path.isdir("./db"):
            os.mkdir("./db")
            FileManager.create_json_files()
            FileManager.create_csv_files()
            FileManager.create_theme_file()

    def load(path: str):
        with open(path) as file:
            return load(file)

    def save_in_json(path: str, data):
        with open(path, "w") as file:
            dump(data, file, indent=4)

    def save_in_csv(path: str, data: list, mode: str = "a"):
        with open(path, mode, newline="") as f:
            wr = writer(
                f,
                delimiter=",",
            )
            for line in data:
                wr.writerow(line)

    def load_theme():
        with open('./db/THEME') as file:
            return file.read()

    def change_theme() -> bool:
        with open('./db/THEME', 'w') as file:
            if theme() == 'PapelerAbasto':
                file.write('Default1')
            else:
                file.write('PapelerAbasto')
        return True


class Sorter:
    class _Sorter:
        def __init__(self):
            pass

    class _StrSorter(_Sorter):
        def field(self, field):
            return field

    class _IntSorter(_Sorter):
        def field(self, field):
            try:
                return int(field)
            except:
                return field

    class _NOMBRE(_StrSorter):
        ...

    class _PU(_IntSorter):
        ...

    class _STOCK(_IntSorter):
        ...

    class _CANTIDAD(_IntSorter):
        ...

    class _PF(_IntSorter):
        ...

    class _PROVEEDOR(_StrSorter):
        ...

    def __init__(self, record_list):
        self._record_list = record_list
        self._index = self._NOMBRE()

    def change_sorter(self):
        self._index = getattr(
            self, '_' + Main.instance()[self.change_sorter].get()
        )()

    def _get_sort_index(self) -> int:
        return cs.SORTER_COMBO_ALL_VALUES[Main.instance()[
            self._record_list.change_sorter].get()]

    def _sort(self, field_calc: callable, field: int, reverse: bool = False):
        self._record_list._update_from_report(
            sorted(
                self._record_list.get_report(),
                key=lambda rc: field_calc(rc[field]),
                reverse=reverse
            )
        )

    def sort_list_min_max(self):
        self._sort(self._index.field, self._get_sort_index())

    def sort_list_max_min(self):
        self._sort(self._index.field, self._get_sort_index(), True)


class Remover:
    class _Remover:
        def __init__(self):
            pass

    class _SELECCIONADOS(_Remover):
        def remove_records(self, rc_list) -> bool:
            if rc_list._have_checked_records():
                for rc in reversed(rc_list.Rows):
                    if rc[0].get_check():
                        rc_list.Rows.remove(rc)
                rc_list.save_in_json()
                return True
            return False

    class _VACÍOS(_Remover):
        def remove_records(self, rc_list) -> bool:
            if rc_list.have_empty_records():
                for rc in reversed(rc_list.Rows):
                    if rc[0].is_empty():
                        rc_list.Rows.remove(rc)
                rc_list.save_in_json()
                return True
            return False

    class _TODOS(_Remover):
        def remove_records(self, rc_list) -> bool:
            if rc_list.Rows:
                rc_list.Rows = []
                return True
            return False

    def __init__(self, record_list):
        self._record_list = record_list
        self._remover = self._SELECCIONADOS()

    def set_remover(self, remover: str):
        self._remover = getattr(self, remover)()
        Main.instance()[self.change_remover].update(remover.strip('_'))

    def change_remover(self):
        self._remover = getattr(
            self, '_' + Main.instance()[self.change_remover].get()
        )()

    def remove_records(self) -> bool:
        return self._remover.remove_records(self._record_list)


class EmptyRecordControl:
    def __init__(self, record_list):
        self._record_list = record_list

    def empty_record_control(self) -> bool:
        for rc in reversed(self._record_list._get_records()):
            if rc.is_empty():
                return True
        return False


class RecordAdder:
    def __init__(self, record_list):
        self._record_list = record_list

    def add_records(self) -> bool:
        how_many_add = int(
            Main.instance()[(
                self._record_list,
                cs.ADDER_SPIN_KEY,
            )].get()
        )
        if how_many_add:
            report = self._record_list.get_report()
            for _ in range(how_many_add):
                report.append(
                    self._record_list.get_class_record().get_empty_report()
                )
            FileManager.save_in_json(
                path=self._record_list.get_json_path(), data=report
            )
            # FileManager.save_in_json(
            #     path=self._record_list.get_json_path(),
            #     data=list(
            #         map(
            #             lambda _: self._record_list.get_report().append(
            #                 self._record_list.get_class_record().get_empty_report()
            #             ), range(how_many_add)
            #         )
            #     )
            # )
            return True
        return False


# ------------------------------ #
#        section_tools.py        #
# ------------------------------ #
class RenderAdder:
    def render_adder(record_list) -> list:
        return [
            Spin(
                key=(
                    record_list,
                    cs.ADDER_SPIN_KEY,
                ),
                size=cs.ADDER_SPIN_SIZE,
                pad=cs.ADDER_SPIN_PAD,
                values=cs.ADDER_SPIN_VALUES,
                initial_value=0,
                readonly=True
            ),
            Button(
                key=record_list.add_records,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.ADDER_BUTTON_PAD,
                button_text=cs.ADDER_BUTTON_TEXT,
                tooltip=cs.ADDER_BUTTON_TOOLTIP
            )
        ]


# ------------------------------ #
#           record.py            #
# ------------------------------ #
class Record(Column):
    @classmethod
    def get_name_size(cls) -> tuple:
        return cls._NAME_SIZE

    @classmethod
    def get_empty_report(cls) -> list:
        return ['', 0, 0]

    def __init__(self, name: str, unit_price: float, stock: int):
        default_fields = [
            [
                self._name_element(name),
                self._unit_price_element(unit_price),
                self._stock_element(stock)
            ]
        ]
        super().__init__(layout=default_fields, pad=cs.RECORD_PAD)

    def _name_element(self, name: str) -> Input:
        return Input(
            default_text=name, size=self.get_name_size(), pad=cs.NAME_PAD
        )

    def _unit_price_element(self, unit_price: float) -> Input:
        return Input(
            default_text=unit_price,
            size=cs.UNIT_PRICE_SIZE,
            pad=cs.UNIT_PRICE_PAD
        )

    def _stock_element(self, stock: int) -> Input:
        return Input(default_text=stock, size=cs.STOCK_SIZE, pad=cs.STOCK_PAD)

    def _percent_element(self, percent: float) -> Spin:
        return Spin(
            values=cs.SPIN_VALUES,
            initial_value=percent,
            readonly=True,
            size=cs.SPIN_SIZE,
            pad=cs.SPIN_PAD
        )

    def _check_element(self, check: bool) -> Checkbox:
        return Checkbox(
            text='',
            default=check,
            pad=cs.CHECK_PAD,
            text_color='Black',
            checkbox_color='White'
        )

    def _add_percent_and_check_elements(self, percent: int, check: bool):
        fields = self._get_fields()
        fields += (self._percent_element(percent), self._check_element(check))

    def _get_fields(self) -> list:
        return self.Rows[0]

    def get_name(self) -> str:
        return self._get_fields()[0].get()

    def get_unit_price(self) -> float:
        return round(float(self._get_fields()[1].get()), 2)

    def get_stock(self) -> int:
        return int(self._get_fields()[2].get())

    def get_percent(self) -> float:
        return round(float(self._get_fields()[-2].get()), 1)

    def get_check(self) -> bool:
        return bool(self._get_fields()[-1].get())

    def get_report(self) -> list:
        return list(map(lambda field: field.get(), self._get_fields()))

    def get_csv_report(self) -> list:
        return list(map(lambda field: field.get(), self._get_fields()[:-2]))

    def have_percent_to_apply(self) -> bool:
        return bool(self.get_percent())

    def name_comparisson(self, name: str) -> bool:
        return self.Rows[0][0].get().upper() == name.upper()

    def indicate_issue(self, index: int, color: str = 'Red'):
        self._get_fields()[index].update(background_color=color)

    def clear_issues(self):
        for field in self._get_fields()[:-2]:
            field.update(background_color='White')

    def update_stock(self, stock: int):
        self._get_fields()[2].update(stock)

    def update_unit_price(self, unit_price: float):
        self._get_fields()[1].update(unit_price)

    def update_from_report(self, report: list):
        fields = self._get_fields()
        for i, field in enumerate(report):
            fields[i].update(field)

    def passes_apply_percent_control(self) -> bool:
        try:
            self.get_unit_price()
            return True
        except:
            self.indicate_issue(1)
            return False

    def clear_percent(self):
        self._get_fields()[-2].update(0)

    def is_empty(self) -> bool:
        return self._get_fields()[0].get() == ''

    def check(self):
        self._get_fields()[-1].update(True)

    def uncheck(self):
        self._get_fields()[-1].update(False)


class StockRecord(Record):
    _NAME_SIZE = cs.STOCK_NAME_SIZE
    _secure_mode = False

    @classmethod
    def get_empty_report(cls) -> list:
        return Record.get_empty_report() + [0, False]

    @classmethod
    def change_secure_mode(cls):
        cls._secure_mode = not cls._secure_mode
        Main.instance()[StockList.instance().secure_mode
                       ].update('🔐' if cls._secure_mode else '🔓')

    def __init__(
        self,
        name: str = '',
        unit_price: float = 0.,
        stock: int = 0,
        percent: int = 0,
        check: bool = False
    ):
        Config.setattr_in_object_from_objects(self, BaseRecordControl(self))
        super().__init__(name, unit_price, stock)
        self._add_percent_and_check_elements(percent, check)

    def passes_pre_sale_control(self) -> bool:
        if self.passes_base_control():
            if self.have_stock():
                if self.have_unit_price():
                    return True
                self.indicate_issue(1)
            else:
                self.indicate_issue(2)
        return False

    def passes_pre_buy_control(self) -> bool:
        if self.passes_base_control():
            if self.have_unit_price():
                return True
            self.indicate_issue(1)
        return False

    def get_pre_commerce_report(self) -> list:
        return list(map(lambda field: field.get(), self._get_fields()[:-2]))

    def able_to_sell(self, amount: int) -> bool:
        return self.get_stock() - amount > -1

    def update_from_buy(self, unit_price: float, amount: int):
        self._get_fields()[1].update(unit_price)
        self._get_fields()[2].update(self.get_stock() + amount)

    def update_from_sale(self, amount: int):
        self.update_stock(self.get_stock() - amount)

    def secure_mode(self):
        for field in self._get_fields():
            field.update(disabled=StockRecord._secure_mode)

    def apply_percent(self):
        if self.passes_apply_percent_control():
            self.update_unit_price(
                round(
                    self.get_unit_price() +
                    self.get_unit_price() * self.get_percent() / 100., 2
                )
            )
            self.clear_percent()

    def have_stock(self) -> bool:
        return self.get_stock() > 0

    def passes_stock_control(self) -> bool:
        try:
            self.get_stock()
            if self.have_stock() > 0:
                return True
        except:
            pass
        self.indicate_issue(2, 'Orange')
        return False


class CommerceRecord(Record):
    def __init__(
        self, name: str, unit_price: float, stock: int, amount: int,
        final_price: float
    ):
        super().__init__(name, unit_price, stock)
        self._get_fields().append(self._amount_element(amount))
        self._get_fields().append(self._final_price_element(final_price))

    def _amount_element(self, amount: int):
        return Input(
            default_text=amount, size=cs.AMOUNT_SIZE, pad=cs.AMOUNT_PAD
        )

    def _final_price_element(self, final_price: float):
        return Input(
            default_text=final_price,
            size=cs.FINAL_PRICE_SIZE,
            pad=cs.FINAL_PRICE_PAD
        )

    def get_amount(self) -> int:
        return int(self._get_fields()[3].get())

    def get_csv_report(self) -> list:
        return ['', '', ''] + super().get_csv_report()

    def get_wrong_field_index(self) -> int:
        error = super().get_wrong_field_index()
        if error == -1:
            try:
                int(self.get_amount())
            except:
                error = 3
        return error

    def update_final_price(self, final_price: float):
        self._get_fields()[4].update(final_price)

    def calculate_final_price(self) -> float:
        price = round(self.get_unit_price() * float(self.get_amount()), 2)
        percent = price * self.get_percent() / 100.
        return round(price + percent, 2)

    def apply_final_price(self) -> float:
        self.clear_issues()
        if self.passes_control():
            final_price = self.calculate_final_price()
            self.update_final_price(final_price)
            return final_price
        return 0


class SaleRecord(CommerceRecord):
    _NAME_SIZE = cs.SALE_NAME_SIZE

    def __init__(
        self,
        name: str = '',
        unit_price: float = 0.,
        stock: int = 0,
        amount: int = 0,
        final_price: float = 0.,
        percent: int = 0,
        check: bool = False
    ):
        super().__init__(name, unit_price, stock, amount, final_price)
        self._add_percent_and_check_elements(percent, check)
        self._make_elements_read_only()

    def _make_elements_read_only(self):
        self._get_fields()[0].ReadOnly = True
        self._get_fields()[1].ReadOnly = True
        self._get_fields()[2].ReadOnly = True
        self._get_fields()[4].ReadOnly = True

    def get_sale_report(self) -> list:
        return [self.get_name(), self.get_amount()]

    def passes_control(self) -> bool:
        try:
            amount = self.get_amount()
            if amount <= self.get_stock():
                return True
        except:
            pass
        self.indicate_issue(3)
        return False


class BuyRecord(CommerceRecord):
    _NAME_SIZE = cs.BUY_NAME_SIZE

    @classmethod
    def get_empty_report(cls) -> list:
        return ['', 0, 0, 0, 0, '', 0, True]

    def __init__(
        self,
        name: str = '',
        unit_price: float = 0.,
        stock: int = 0,
        amount: int = 0,
        final_price: float = 0.,
        supplier: str = '',
        percent: int = 0,
        check: bool = False
    ):
        Config.setattr_in_object_from_objects(self, BaseRecordControl(self))
        super().__init__(name, unit_price, stock, amount, final_price)
        self._get_fields().append(self._supplier_element(supplier))
        self._add_percent_and_check_elements(percent, check)
        self._make_elements_read_only()

    def _supplier_element(self, supplier):
        return Input(
            default_text=supplier, size=cs.SUPPLIER_SIZE, pad=cs.SUPPLIER_PAD
        )

    def _make_elements_read_only(self):
        self._get_fields()[4].ReadOnly = True

    def get_buy_report(self) -> list:
        return [self.get_name(), self.get_unit_price(), self.get_amount()]

    def passes_control(self) -> bool:
        if self.passes_base_control():
            try:
                self.get_amount()
            except:
                self.indicate_issue(3)
                return False
            return True

    def passes_control_for_calculate_final_price(self) -> int:
        error = 0
        try:
            error = 1
            self.get_unit_price()
            if not self.have_unit_price():
                raise Exception
            error = 3
            self.get_amount()
        except:
            self.indicate_issue(error)
            return False
        return True


# ------------------------------ #
#         record_list.py         #
# ------------------------------ #
class RecordList(Column):
    __instance = None

    @classmethod
    def instance(cls):
        if not cls.__instance:
            cls.__instance = cls.new()
        return cls.__instance

    def __init__(self, records: list, size: tuple, pad=tuple):
        Config.setattr_in_object_from_objects(self, Sorter(self), Remover(self))
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
            rc.update_from_report(report[i])

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

    def get_search_index(self, name: str) -> int:
        for i, rc in enumerate(self._get_records()):
            if rc.name_comparisson(name):
                return i
        raise IndexError

    def search(self):
        name = Main.instance()[(
            self,
            'finder_input',
        )].get()
        rcs = self._get_records()
        index = self.get_search_index(name)
        rc_to_top = rcs[index].get_report()
        for i in reversed(range(1, index + 1)):
            rcs[i].update_from_report(rcs[i - 1].get_report())
        rcs[0].update_from_report(rc_to_top)

    def uncheck_records(self):
        for rc in self.get_checked_records():
            rc.uncheck()

    def clear_issues(self):
        for rc in self._get_records():
            rc.clear_issues()

    def check_all(self):
        for rc in self._get_records():
            rc.check()

    def save_in_json(self):
        FileManager.save_in_json(self.get_json_path(), self.get_report())


class StockList(RecordList):
    @classmethod
    def new(cls):
        records = [
            [StockRecord(name, unit_price, stock, percent, check)]
            for name, unit_price, stock, percent, check in
            FileManager.load(path=cs.JSON_STOCK_PATH)
        ]
        return cls(records)

    def __init__(self, records: list):
        Config.setattr_in_object_from_objects(
            self, RecordAdder(self), EmptyRecordControl(self)
        )
        super().__init__(
            records=records,
            size=cs.RECORDLIST_COLUMN_SIZE,
            pad=cs.RECORDLIST_COLUMN_PAD,
        )

    def get_json_path(self) -> str:
        return cs.JSON_STOCK_PATH

    def get_csv_report(self) -> list[list]:
        return cs.CSV_STOCK_HEADER + list(
            map(lambda rc: rc.get_csv_report(), self._get_records())
        )

    def get_class_record(self) -> Record:
        return StockRecord

    def passes_pre_commerce_control(self, control: str) -> bool:
        if self._have_checked_records():
            self.clear_issues()
            for rc in self.get_checked_records():
                if not getattr(rc, control)():
                    return False
            return True
        return False

    def passes_pre_sale_control(self) -> bool:
        return self.passes_pre_commerce_control('passes_pre_sale_control')

    def passes_pre_buy_control(self) -> bool:
        return self.passes_pre_commerce_control('passes_pre_buy_control')

    def passes_stock_control(self):
        self.clear_issues()
        for rc in self.get_checked_records():
            rc.passes_stock_control()

    def apply(self):
        self.clear_issues()
        for rc in tuple(
            filter(
                lambda rc: rc.passes_apply_percent_control() and rc.
                have_percent_to_apply(), self._get_records()
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
            record.update_from_buy(buy_report[1], buy_report[2])
            return False
        return True

    def complete_buy_report(self, buys_report: list):
        for buy_report in buys_report:
            buy_report += [0, False]

    def receive_buys_report(self, buys_report: list):
        filtered_buys_report = list(
            filter(self.update_record_from_buy_report, buys_report)
        )
        if filtered_buys_report:
            self.complete_buy_report(filtered_buys_report)
            self.add_records_from_buys_report(filtered_buys_report)
        else:
            self.save_in_json()

    def update_record_from_sale_report(self, sale_report: list):
        self.get_record(sale_report[0]).update_from_sale(sale_report[1])

    def receive_sales_report(self, sales_report: list):
        for sale_report in sales_report:
            self.update_record_from_sale_report(sale_report)
        self.save_in_json()

    def export(self):
        print(Main.instance().ReturnValuesDictionary[self.export])
        FileManager.save_in_csv(
            path=Main.instance().ReturnValuesDictionary[self.export],
            data=self.get_csv_report(),
            mode="w"
        )

    def get_pre_commerce_report(self) -> list[list]:
        return list(
            map(
                lambda rc: rc.get_pre_commerce_report(),
                self.get_checked_records()
            )
        )

    def pre_commerce(
        self, pre_commerce_control: callable, where_to_trade: callable
    ) -> bool:
        self.save_in_json()
        if pre_commerce_control():
            return where_to_trade.instance().pre_commerce_from_report(
                self.get_pre_commerce_report()
            )
        return False

    def pre_sell(self) -> bool:
        return self.pre_commerce(self.passes_pre_sale_control, SaleList)

    def pre_buy(self) -> bool:
        return self.pre_commerce(self.passes_pre_buy_control, BuyList)

    def secure_mode(self):
        StockRecord.change_secure_mode()
        for rc in self._get_records():
            rc.secure_mode()

    def have_record(self, name: str) -> bool:
        if self.get_record(name):
            return True
        return False

    def collect_value(self, name: str, value_method: str) -> tuple:
        return (name, getattr(self.get_record(name), value_method)())

    def collect_values(self, names: tuple, collect_method: str) -> tuple:
        return tuple(
            map(
                getattr(self, collect_method),
                list(set(self.get_record_names()).intersection(set(names)))
            )
        )

    def collect_unit_price_from_record_name(self, name: str) -> tuple:
        return self.collect_value(name, 'get_unit_price')

    def collect_unit_price_from_record_names(self, names: tuple) -> tuple:
        return self.collect_values(names, 'collect_unit_price_from_record_name')

    def collect_stock_from_record_name(self, name: str) -> tuple:
        return self.collect_value(name, 'get_stock')

    def collect_stock_from_record_names(self, names: tuple) -> tuple:
        return self.collect_values(names, 'collect_stock_from_record_name')

    def passes_buy_control(self, record_names: tuple) -> bool:
        control = True
        self.clear_issues()
        for record_name in record_names:
            record = self.get_record(record_name)
            if record:
                if record.passes_base_control():
                    control = True
                else:
                    return False
        return control

    def passes_sale_control(self, record_names: tuple) -> bool:
        control = True
        self.clear_issues()
        for record_name in record_names:
            record = self.get_record(record_name)
            if record:
                if record.passes_base_control():
                    if not record.have_stock():
                        record.indicate_issue(2)
                        return False
                    control = True
                else:
                    return False
            else:
                return False
        return control


class CommerceList(RecordList):
    def __init__(self, records: list, size: tuple, pad: tuple):
        super().__init__(records=records, size=size, pad=pad)

    def get_sale_report(self) -> list:
        return list(map(lambda rc: (rc.get_sale_report()), self._get_records()))

    def get_buy_report(self) -> list:
        return list(map(lambda rc: (rc.get_buy_report()), self._get_records()))

    def get_csv_report(self) -> list[list]:
        header = cs.CSV_HEADER
        header[0].append(self.apply())
        return header + list(
            map(lambda rc: rc.get_csv_report(), self._get_records())
        )

    def save_in_csv(self):
        FileManager.save_in_csv(
            path=self.get_csv_path(), data=self.get_csv_report()
        )

    def export(self):
        path = Main.instance().ReturnValuesDictionary[self.export]
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
            existent_record.update_from_report(report)
            return False
        return True

    def calculate_total_price(self) -> float:
        return sum(
            tuple(map(lambda rc: rc.apply_final_price(), self._get_records()))
        )

    def apply(self):
        Main.instance()[(
            self,
            'total_price',
        )].update(self.calculate_total_price())

    def pre_commerce_from_report(self, report: tuple) -> bool:
        filtered_report = list(filter(self.update_existent_record, report))
        if filtered_report:
            self.complete_pre_sell_report(filtered_report)
            FileManager.save_in_json(
                path=self.get_json_path(),
                data=filtered_report + self.get_report()
            )
            return True
        return False

    def passes_amount_control(self) -> bool:
        for rc in self.get_checked_records():
            if not rc.get_amount() > 0:
                rc.indicate_issue(3)
                return False
        return True

    def get_checked_record_names(self) -> tuple[str]:
        return tuple(map(lambda rc: rc.get_name(), self.get_checked_records()))

    def remove_checked_records(self) -> bool:
        self.set_remover('_SELECCIONADOS')
        self.remove_records()

    def _collect(self, collect_method: str, update_method: str):
        for rc in getattr(StockList.instance(),
                          collect_method)(self.get_record_names()):
            getattr(self.get_record(rc[0]), update_method)(rc[1])

    def _collect_unit_prices(self):
        self._collect(
            'collect_unit_price_from_record_names', 'update_unit_price'
        )

    def _collect_stock(self):
        self._collect('collect_stock_from_record_names', 'update_stock')

    def collect(self):
        self._collect_stock()
        self._collect_unit_prices()

    def check_all(self):
        tuple(map(lambda rc: rc[0].check(), self.Rows))


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

    def existence_control(self) -> bool:
        for rc in self.get_checked_records():
            if not StockList.instance().have_record(rc.get_name()):
                # rc.indicate_issue(0, 'Orange') NO SE PUEDE ACTUALIZAR EL COLOR DE UN INPUT READOLNY, EN TODO CASO INVESTIGAR
                return False
        return True

    def commerce(self):
        if self.existence_control():
            if self.passes_control():
                if self.passes_amount_control():
                    if StockList.instance().passes_sale_control(
                        self.get_checked_record_names()
                    ):
                        self.apply()
                        self.upload_commerce_report()
                        self.save_in_csv()
                        self.remove_checked_records()
                        self.save_in_json()
                        return True
        return False


class BuyList(CommerceList):
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
        Config.setattr_in_object_from_objects(
            self, RecordAdder(self), EmptyRecordControl(self)
        )
        super().__init__(
            records=records,
            size=cs.BUYLIST_COLUMN_SIZE,
            pad=cs.BUYLIST_COLUMN_PAD
        )

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

    def complete_pre_sell_report(self, pre_sell_report: list):
        for report in pre_sell_report:
            report += [0, 0, '', 0, False]

    def commerce(self) -> bool:
        if self.passes_control():
            if self.passes_amount_control():
                if StockList.instance().passes_buy_control(
                    self.get_checked_record_names()
                ):
                    self.apply()
                    self.upload_commerce_report()
                    self.save_in_csv()
                    self.remove_checked_records()
                    self.save_in_json()
                    return True
        return False


# ------------------------------ #
#             gui.py             #
# ------------------------------ #
class Section(Column):
    __instance = None

    @classmethod
    def instance(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance

    @classmethod
    def get_index_name_size(cls) -> tuple:
        return cls._INDEX_NAME_SIZE

    @classmethod
    def get_remover_options(cls) -> list:
        return cls._REMOVER_OPTIONS

    @classmethod
    def key(cls, key):
        cls.__key = key

    def __init__(self, size: tuple, pad: tuple):
        super().__init__(layout=self.render_layout(), size=size, pad=pad)

    def __len__(self) -> int:
        return len(self.get_record_list())

    def render_finder(self) -> list:
        return [
            Input(
                key=(
                    self._record_list,
                    'finder_input',
                ),
                size=cs.FINDER_INPUT_SIZE,
                pad=cs.FINDER_INPUT_PAD
            ),
            Button(
                key=self._record_list.search,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.FINDER_BUTTON_PAD,
                button_text=cs.FINDER_BUTTON_TEXT,
                tooltip=cs.FINDER_BUTTON_TOOLTIP
            )
        ]

    def render_sorter(self) -> list:
        sort_values = self.get_sort_values()
        return [
            Combo(
                key=self._record_list.change_sorter,
                values=sort_values,
                default_value=sort_values[0],
                size=cs.SORTER_COMBO_SIZE,
                pad=cs.SORTER_COMBO_PAD,
                tooltip=cs.SORTER_COMBO_TOOLTIP,
                readonly=True,
                enable_events=True
            ),
            Button(
                key=self._record_list.sort_list_min_max,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.SORTER_BUTTON_PAD,
                button_text=cs.SORTER_BUTTON_UP_TEXT,
                tooltip=cs.SORTER_BUTTON_UP_TOOLTIP
            ),
            Button(
                key=self._record_list.sort_list_max_min,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.SORTER_BUTTON_PAD,
                button_text=cs.SORTER_BUTTON_DOWN_TEXT,
                tooltip=cs.SORTER_BUTTON_DOWN_TOOLTIP
            )
        ]

    def render_remover(self) -> list:
        remover_options = self.get_remover_options()
        return [
            Combo(
                key=self._record_list.change_remover,
                size=cs.REMOVER_COMBO_SIZE,
                pad=cs.REMOVER_COMBO_PAD,
                values=remover_options,
                default_value=remover_options[0],
                readonly=True,
                enable_events=True
            ),
            Button(
                key=self._record_list.remove_records,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.REMOVER_BUTTON_PAD,
                button_text=cs.REMOVER_BUTTON_TEXT,
                tooltip=cs.REMOVER_BUTTON_TOOLTIP
            )
        ]

    def render_apply(self) -> list:
        return [
            Button(
                key=self._record_list.apply,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.APPLY_BUTTON_PAD,
                button_text=cs.APPLY_BUTTON_TEXT,
                tooltip=cs.APPLY_BUTTON_TOOLTIP
            )
        ]

    def render_base_index(
        self, input_size: tuple, input_pad: tuple, default_text: str
    ) -> list:
        index = [
            [
                Input(
                    size=input_size,
                    pad=input_pad,
                    default_text=default_text,
                    readonly=True
                )
            ]
        ]
        return [
            Column(
                layout=index,
                pad=cs.INDEX_COLUMN_PAD,
                element_justification='center'
            )
        ]

    def render_name_index(self) -> list:
        return self.render_base_index(
            self.get_index_name_size(), cs.INDEX_INPUT_NAME_PAD,
            cs.INDEX_INPUT_NAME_TEXT
        )

    def render_unit_price_index(self) -> list:
        return self.render_base_index(
            cs.INDEX_INPUT_UNIT_PRICE_SIZE, cs.INDEX_INPUT_UNIT_PRICE_PAD,
            cs.INDEX_INPUT_UNIT_PRICE_TEXT
        )

    def render_stock_index(self) -> list:
        return self.render_base_index(
            cs.INDEX_INPUT_STOCK_SIZE, cs.INDEX_INPUT_STOCK_PAD,
            cs.INDEX_INPUT_STOCK_TEXT
        )

    def render_percent_index(self) -> list:
        return self.render_base_index(
            cs.INDEX_INPUT_PERCENT_SIZE, cs.INDEX_INPUT_PERCENT_PAD,
            cs.INDEX_INPUT_PERCENT_TEXT
        )

    def render_index(self) -> list:
        index = self.render_name_index()
        index += self.render_unit_price_index()
        index += self.render_stock_index()
        return index

    def render_save_as(self) -> list:
        return [
            SaveAs(
                key=self._record_list.export,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.SAVE_AS_BUTTON_PAD,
                button_text=cs.SAVE_AS_BUTTON_TEXT,
                tooltip=cs.SAVE_AS_BUTTON_TOOLTIP,
                file_types=(('.csv', ''), ),
                default_extension='.csv',
                initial_folder=cs.SAVE_AS_BUTTON_INITIAL_FOLDER,
                target=(555666777, 0)
            )
        ]

    def render_uncheck(self) -> list:
        return [
            Button(
                key=self._record_list.uncheck_records,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_LITTLE_IMAGE_SIZE,
                pad=cs.UNCHECK_BUTTON_PAD,
                button_text=cs.UNCHECK_BUTTON_TEXT,
                tooltip=cs.UNCHECK_BUTTON_TOOLTIP
            )
        ]

    def render_record_list(self) -> list:
        return [self._record_list]

    def render_layout(self) -> list:
        """
        [
            [finder, sorter, REMOVER, adder, save_as],
            [index, apply],
            [record_list]
        ]
        """
        layout = []
        layout.append(self.render_finder())
        layout[0] += self.render_sorter()
        layout[0] += self.render_remover()
        layout.append(self.render_save_as())
        layout.append(self.render_index())
        layout[1] += self.render_apply()
        layout[2] += self.render_uncheck()
        layout.append(self.render_record_list())
        return layout

    def get_save_target(self) -> int:
        return cs.DEFAULT_SAVE_TARGET


class StockSection(Section):
    _INDEX_NAME_SIZE = cs.INDEX_INPUT_STOCK_NAME_SIZE
    _REMOVER_OPTIONS = cs.STOCK_SECTION_REMOVER_OPTIONS

    @classmethod
    def get_sort_values(cls) -> list:
        return cs.SORTER_COMBO_STOCK_VALUES

    @classmethod
    def get_record_list(cls) -> StockList:
        return StockList.instance()

    def __init__(self):
        self._record_list = StockList.instance()
        super().__init__(cs.STOCKLIST_S_SIZE, cs.STOCKLIST_S_PAD)

    def render_pre_commerce(self) -> list:
        return [
            Button(
                key=self._record_list.pre_buy,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.PRE_BUY_BUTTON_PAD,
                button_text=cs.PRE_BUY_BUTTON_TEXT,
                tooltip=cs.PRE_BUY_BUTTON_TOOLTIP
            ),
            Button(
                key=self._record_list.pre_sell,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.PRE_SELL_BUTTON_PAD,
                button_text=cs.PRE_SELL_BUTTON_TEXT,
                tooltip=cs.PRE_SELL_BUTTON_TOOLTIP
            )
        ]

    def render_index(self) -> list:
        index = super().render_index()
        index += self.render_percent_index()
        return index

    def render_list(self) -> list:
        return [StockList.instance()]

    def render_theme(self) -> list:
        return [
            Button(
                key=FileManager.change_theme,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.THEME_BUTTON_PAD,
                button_text=cs.THEME_BUTTON_NIGHT_TEXT if theme() == 'PapelerAbasto' else cs.THEME_BUTTON_DAY_TEXT,
                tooltip=cs.THEME_BUTTON_TOOLTIP
            )
        ]

    def render_secure_mode(self) -> list:
        return [
            Button(
                key=self._record_list.secure_mode,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.SECURE_MODE_BUTTON_PAD,
                button_text=cs.SECURE_UNLOCK_MODE_BUTTON_TEXT,
                tooltip=cs.SECURE_MODE_BUTTON_TOOLTIP
            )
        ]

    def render_layout(self) -> list:
        layout = super().render_layout()
        adder = RenderAdder.render_adder(self._record_list)
        layout[0].insert(7, adder[0])
        layout[0].insert(8, adder[1])
        layout[1] += self.render_pre_commerce()
        layout[1] += self.render_secure_mode()
        layout[1] += self.render_theme()
        return layout

    def get_save_target(self) -> int:
        return 12


class CommerceSection(Section):
    @classmethod
    def render_layout_in_tab(cls) -> Tab:
        layout = [[cls.instance()]]
        return Tab(
            cls.get_tab_title(),
            layout,
            pad=cs.TAB_PAD,
            border_width=cs.TAB_BORDER_WIDTH
        )

    def __init__(self, size: tuple, pad: tuple):
        super().__init__(size, pad)

    def render_amount_index(self) -> list:
        return super().render_base_index(
            cs.INDEX_INPUT_AMOUNT_SIZE, cs.INDEX_INPUT_AMOUNT_PAD,
            cs.INDEX_INPUT_AMOUNT_TEXT
        )

    def render_final_price_index(self) -> list:
        return self.render_base_index(
            cs.INDEX_INPUT_FINAL_PRICE_SIZE, cs.INDEX_INPUT_FINAL_PRICE_PAD,
            cs.INDEX_INPUT_FINAL_PRICE_TEXT
        )

    def render_index(self) -> list:
        index = super().render_index()
        index += self.render_amount_index()
        index += self.render_final_price_index()
        return index

    def render_commerce(self) -> list:
        return [
            Button(
                key=self._record_list.commerce,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.COMMERCE_BUTTON_PAD,
                button_text=cs.COMMERCE_BUTTON_TEXT,
                tooltip=cs.COMMERCE_BUTTON_TOOLTIP
            ),
            Text(
                key=(
                    self._record_list,
                    'total_price',
                ),
                size=cs.TOTAL_PRICE_SIZE,
                pad=cs.TOTAL_PRICE_PAD
            )
        ]

    def render_collect(self) -> list:
        return [
            Button(
                key=self._record_list.collect,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_IMAGE_SIZE,
                pad=cs.COLLECT_BUTTON_PAD,
                button_text=cs.COLLECT_BUTTON_TEXT,
                tooltip=cs.COLLECT_BUTTON_TOOLTIP
            )
        ]

    def render_check_all(self) -> list:
        return [
            Button(
                key=self._record_list.check_all,
                image_data=cs.BUTTON_IMAGE,
                image_size=cs.BUTTON_LITTLE_IMAGE_SIZE,
                pad=cs.CHECK_ALL_BUTTON_PAD,
                button_text=cs.CHECK_ALL_BUTTON_TEXT,
                tooltip=cs.CHECK_ALL_BUTTON_TOOLTIP
            )
        ]

    def render_layout(self) -> list:
        """
        [
            [
                finder, sorter, REMOVER, save_as,
                pre_visualizator, cs.total_price, commerce
            ],
            [index, apply],
            [record_list]
        ]
        """
        layout = super().render_layout()
        layout[1] += self.render_collect()
        layout[1] += self.render_commerce()
        layout[2] += self.render_check_all()
        return layout


class SaleSection(CommerceSection):
    _INDEX_NAME_SIZE = cs.INDEX_INPUT_SALE_NAME_SIZE
    _REMOVER_OPTIONS = cs.SALE_SECTION_REMOVER_OPTIONS

    @classmethod
    def get_sort_values(cls) -> list:
        return cs.SORTER_COMBO_SALES_VALUES

    @classmethod
    def get_tab_title(cls) -> str:
        return 'VENTAS'

    @classmethod
    def get_record_list(self) -> RecordList:
        return SaleList.instance()

    def __init__(self):
        self._record_list = SaleList.instance()
        super().__init__(cs.SALELIST_S_SIZE, cs.SALELIST_S_PAD)

    def render_index(self) -> list:
        index = super().render_index()
        index += self.render_percent_index()
        return index

    def get_save_target(self) -> int:
        return 8


class BuySection(CommerceSection):
    _INDEX_NAME_SIZE = cs.INDEX_INPUT_BUY_NAME_SIZE
    _REMOVER_OPTIONS = cs.STOCK_SECTION_REMOVER_OPTIONS

    @classmethod
    def get_sort_values(cls) -> list:
        return cs.SORTER_COMBO_BUYS_VALUES

    @classmethod
    def get_tab_title(cls) -> str:
        return 'COMPRAS'

    @classmethod
    def get_record_list(cls):
        return BuyList.instance()

    def __init__(self):
        self._record_list = BuyList.instance()
        super().__init__(cs.BUYSECTION_S_SIZE, cs.BUYSECTION_S_PAD)

    def render_supplier_index(self) -> list:
        return CommerceSection.render_base_index(
            self, cs.INDEX_INPUT_SUPPLIER_SIZE, cs.INDEX_INPUT_SUPPLIER_PAD,
            cs.INDEX_INPUT_SUPPLIER_TEXT
        )

    def render_index(self) -> list:
        index = CommerceSection.render_index(self)
        index += self.render_supplier_index()
        index += self.render_percent_index()
        return index

    def render_layout(self) -> list:
        layout = super().render_layout()
        adder = RenderAdder.render_adder(self._record_list)
        layout[0].insert(8, adder[0])
        layout[0].insert(8, adder[1])
        return layout

    def get_save_target(self) -> int:
        return 10


# ------------------------------ #
#          __init__.py           #
# ------------------------------ #
# - hacer la parte visual(
#       la idea es poner el uncheck a la der del indice, pero mas chiquito, y un check_all con igual tamaño y pegado, el boton con tilde subirlo y cambiarle el nombre porque el tilde va para el check_all
# )
# - hacer que el botón de guardado una vez que guarde el archvio csv, lo ejecute
# - solucionar export
# - Falta solucionar el total en la carga de compra y venta (el total en el csv)
class Main(Window):
    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        FileManager.db_control()
        self.load_theme()
        super().__init__(
            self.render_layout(),
            font=('Helvetica 16'),
            size=cs.WINDOWS_SIZE,
            location=cs.WINDOWS_LOCATION
        )

    def render_layout(self) -> list[list]:
        tab_group = [
            [
                SaleSection.render_layout_in_tab(),
                BuySection.render_layout_in_tab()
            ]
        ]
        layout = [
            [StockSection.instance()],
            [
                TabGroup(
                    tab_group,
                    pad=cs.TAB_GROUP_PAD,
                    border_width=cs.TAB_GROUP_BORDER_WIDTH
                )
            ]
        ]
        return layout

    def load_theme(self):
        theme(FileManager.load_theme())

    def close(self, timeout=0):
        self.read(timeout=timeout)
        super().close()
        exit()

    def restart(self):
        Process(target=FileManager.restart).start()
        self.close(2000)

    def save(self):
        StockList.instance().save_in_json()
        SaleList.instance().save_in_json()
        BuyList.instance().save_in_json()

    def run(self):
        while True:
            e, _ = self.read()
            print('evento:', e)
            try:
                if e():
                    self.restart()
            except:
                if e == '__EXIT__':
                    self.save()
                    self.close()
                    break
                if e is None:
                    self.close()
                    break
                print('error')


if __name__ == '__main__':
    Main.instance().run()
