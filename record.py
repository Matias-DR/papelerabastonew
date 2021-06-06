from PySimpleGUI import (theme, Window, Column, Input, Spin, Checkbox, Button)
import constants as cs


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
        super().__init__(layout=default_fields)

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
            text='', default=check, pad=cs.CHECK_PAD, checkbox_color='White'
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

    def passes_stock_control(self) -> bool:
        try:
            self.get_stock()
            if self.have_stock() > 0:
                return True
        except:
            pass
        self.indicate_issue(2, 'Orange')
        return False


class StockAndBuyRecord:
    def passes_control(self) -> bool:
        if self.get_name() == '':
            self.indicate_issue(0)
            return False
        try:
            error = 1
            self.get_unit_price()
            error = 2
            self.get_stock()
        except:
            self.indicate_issue(error)
            return False
        return True

    def have_unit_price(self) -> bool:
        return self.get_unit_price() > 0


class StockRecord(Record, StockAndBuyRecord):
    _NAME_SIZE = cs.STOCK_NAME_SIZE
    _secure_mode = False

    @classmethod
    def get_empty_report(cls) -> list:
        return Record.get_empty_report() + [0, False]

    @classmethod
    def change_secure_mode(cls):
        cls._secure_mode = not cls._secure_mode

    def __init__(
        self,
        name: str = '',
        unit_price: float = 0.,
        stock: int = 0,
        percent: int = 0,
        check: bool = False
    ):
        Record.__init__(self, name, unit_price, stock)
        StockAndBuyRecord.__init__(self)
        self._add_percent_and_check_elements(percent, check)

    def passes_pre_sale_control(self) -> bool:
        if self.passes_control():
            if self.have_stock():
                if self.have_unit_price():
                    return True
                self.indicate_issue(1)
            else:
                self.indicate_issue(2)
        return False

    def passes_pre_buy_control(self) -> bool:
        if self.passes_control():
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
        return ['', ''] + super().get_csv_report()

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
        final_price = self.calculate_final_price()
        self.update_final_price(final_price)
        return final_price


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


class BuyRecord(CommerceRecord, StockAndBuyRecord):
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
        CommerceRecord.__init__(
            self, name, unit_price, stock, amount, final_price
        )
        StockAndBuyRecord.__init__(self)
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
        if StockAndBuyRecord.passes_control(self):
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
