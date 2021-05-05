from PySimpleGUI import (
    theme, Window, Column, Input, Spin, Checkbox, Button
)
from constants import (
    NAME_ELEMENT_SIZE, NAME_ELEMENT_PAD, UNIT_PRICE_ELEMENT_SIZE, UNIT_PRICE_ELEMENT_PAD,
    STOCK_ELEMENT_SIZE, STOCK_ELEMENT_PAD, SPIN_ELEMENT_VALUES, SPIN_ELEMENT_SIZE,
    SPIN_ELEMENT_PAD, CHECK_ELEMENT_PAD, AMOUNT_ELEMENT_SIZE, AMOUNT_ELEMENT_PAD,
    FINAL_PRICE_ELEMENT_SIZE, FINAL_PRICE_ELEMENT_PAD, SUPPLIER_ELEMENT_SIZE,
    SUPPLIER_ELEMENT_PAD, BUTTON_BORDER_WIDTH
)


class Record(Column):
    """
    Superclase que define elementos predeterminados para todo registro
    """
    def __init__(self, name: str, unit_price: float, stock: int):
        """
        :key: Clave del registro\n
        :name: Nombre del registro\n
        :unit_price: Precio unitario del registro\n
        :stock: Stock del registro\n
        """
        default_fields = [
            [
                self._name_element(name),
                self._unit_price_element(unit_price),
                self._stock_element(stock)
            ]
        ]
        super().__init__(layout=default_fields)

    def _name_element(self, name: str):
        return Input(default_text=name,
                     size=NAME_ELEMENT_SIZE,
                     pad=NAME_ELEMENT_PAD)

    def _unit_price_element(self, unit_price: float):
        return Input(default_text=unit_price,
                     size=UNIT_PRICE_ELEMENT_SIZE,
                     pad=UNIT_PRICE_ELEMENT_PAD)

    def _stock_element(self, stock: int):
        return Input(default_text=stock,
                     size=STOCK_ELEMENT_SIZE,
                     pad=STOCK_ELEMENT_PAD)

    def _percent_element(self, percent: float):
        return Spin(values=SPIN_ELEMENT_VALUES,
                    initial_value=percent,
                    readonly=True,
                    size=SPIN_ELEMENT_SIZE,
                    pad=SPIN_ELEMENT_PAD)

    def _check_element(self, check: bool):
        return Checkbox(text='',
                        default=check,
                        pad=CHECK_ELEMENT_PAD,
                        checkbox_color='White')

    def _add_percent_and_check_elements(self, percent: int, check: bool):
        self.Rows[0].append(self._percent_element(percent))
        self.Rows[0].append(self._check_element(check))

    def get_name(self):
        """
        :return: String
        """
        return self.Rows[0][0].get()

    def get_unit_price(self):
        """
        :return: Float
        """
        return round(float(self.Rows[0][1].get()), 2)

    def get_stock(self):
        """
        :return: Integer
        """
        return int(self.Rows[0][2].get())

    def get_percent(self):
        """
        :return: Float
        """
        percent = round(float(self.Rows[0][-2].get()), 1)
        return percent

    def get_fields(self):
        """
        :return: List[Fields]
        """
        return self.Rows[0]

    def is_checked(self):
        """
        :return: Boolean
        """
        return bool(self.Rows[0][-1].get())

    def have_percent_to_apply(self):
        """
        :return: Boolean
        """
        return self.Rows[0][-2].get()

    def get_report(self):
        """
        Valores en pantalla de cada campo\n
        :return: List[Fields]
        """
        return [
            field.get() for field in self.Rows[0]
        ]

    def get_default_report(self):
        """
        Valores predeterminados de cada campo (con los que fueron creados)\n
        :return: List[Fields]
        """
        report = [
            field.DefaultText for field in self.Rows[0][:-2]
        ]
        report.append(self.Rows[0][-2].DefaultValue)
        report.append(self.Rows[0][-1].InitialState)
        return report

    def is_empty(self):
        """
        :return: Boolean
        """
        return self.Rows[0][0].get() == ''

    def get_error_status(self):
        """
        Retorna el índice del campo en el que se encuentra el error\n
        :return: Integer
        """
        if self.get_name() == '':
            return 0
        try:
            error = 1
            self.get_unit_price()
            error = 2
            self.get_stock()
        except:
            return error
        return -1

    def indicate_error(self, index: int):
        """
        Actualiza el estado del campo indicado hacia error
        """
        self.Rows[0][index].update(background_color='Red')

    def solve_error(self):
        """
        Actualiza el estado de cada campo hacia resuelto
        """
        for field in self.Rows[0][:-2]:
            field.update(background_color='White')

    def remove_percent(self):
        self.Rows[0][-2].update(0)

    def update_unit_price(self, unit_price: float):
        self.Rows[0][1].update(unit_price)

    def update_from_report(self, report: list):
        for i, field in enumerate(self.Rows[0]):
            field.update(report[i])


class StockRecord(Record):
    _secure_mode = False

    @classmethod
    def change_secure_mode(cls):
        cls._secure_mode = not cls._secure_mode

    @classmethod
    def get_empty_report(cls):
        """
        :return: List[Fields]
        """
        return ['', 0, 0, 0, False]

    def __init__(self, name: str='',
                 unit_price: float=0.,
                 stock: int=0, percent: int=0,
                 check: bool=False):
        super().__init__(name, unit_price, stock)
        self._add_percent_and_check_elements(percent, check)

    def secure_mode(self):
        """
        Habilita/ deshabilita los campos en cada registro
        """
        StockRecord._secure_mode = not StockRecord._secure_mode
        for field in self.Rows[0]:
            field.update(disabled=StockRecord._secure_mode)

    def update_from_buy(self, unit_price: float, amount: int):
        self.Rows[0][1].update(unit_price)
        new_stock = self.get_stock() + amount
        self.Rows[0][2].update(new_stock)

    def abble_to_sell(self, amount: int):
        """
        :return: Boolean
        """
        return self.get_stock() - amount > -1

    def update_stock(self, stock: int):
        self.Rows[0][2].update(stock)

    def update_from_sale(self, amount: int):
        self.update_stock(self.get_stock() - amount)

    def apply_percent(self):
        percent = self.get_unit_price() * self.get_percent() / 100.
        self.update_unit_price(round(self.get_unit_price() + percent, 2))

    def uncheck(self):
        self.Rows[0][-1].update(False)


class CommerceRecord(Record):
    """
    Define los elementos y acciones de comercio en común entre los registros de venta y compra
    """
    def __init__(self, name: str, unit_price: float, stock: int, amount: int, final_price: float):
        super().__init__(name, unit_price, stock)
        self.Rows[0].append(self._amount_element(amount))
        self.Rows[0].append(self._final_price_element(final_price))

    def _amount_element(self, amount: int):
        return Input(default_text=amount,
                     size=AMOUNT_ELEMENT_SIZE,
                     pad=AMOUNT_ELEMENT_PAD)

    def _final_price_element(self, final_price: float):
        return Input(default_text=final_price,
                     size=FINAL_PRICE_ELEMENT_SIZE,
                     pad=FINAL_PRICE_ELEMENT_PAD)

    def get_error_status(self):
        """
        Retorna el índice del campo en el que se encuentra el error\n
        :return: Integer
        """
        error = Record.get_error_status(self)
        if error == -1:
            try:
                int(self.get_amount())
            except:
                error = 3
        return error

    def get_amount(self):
        """
        :return: Integer
        """
        return int(self.Rows[0][3].get())

    def update_final_price(self, final_price: float):
        self.Rows[0][4].update(final_price)

    def calculate_final_price(self):
        """
        :return: Float
        """
        price = round(self.get_unit_price() * float(self.get_amount()), 2)
        percent = price * self.get_percent() / 100.
        return round(price + percent, 2)

    def apply_final_price(self):
        """
        :return: Float
        """
        final_price = self.calculate_final_price()
        self.update_final_price(final_price)
        return final_price

    def get_csv_report(self):
        """
        Inserta dos campos vacíos al inicio del reporte\n
        :return: List[Fields]
        """
        csv_report = ['', ''] + self.get_report()
        return csv_report


class SaleRecord(CommerceRecord):
    def __init__(self, name: str='',
                 unit_price: float=0.,
                 stock: int=0,
                 amount: int=0,
                 final_price: float=0.,
                 percent: int=0,
                 check: bool=False):
        super().__init__(name, unit_price, stock, amount, final_price)
        self._add_percent_and_check_elements(percent, check)
        self._make_elements_read_only()

    def _make_elements_read_only(self):
        self.Rows[0][0].ReadOnly = True
        self.Rows[0][1].ReadOnly = True
        self.Rows[0][2].ReadOnly = True
        self.Rows[0][4].ReadOnly = True


class BuyRecord(CommerceRecord):
    def __init__(self, name: str='',
                 unit_price: float=0.,
                 stock: int=0,
                 amount: int=0,
                 final_price: float=0.,
                 supplier: str='',
                 percent: int=0,
                 check: bool=False):
        super().__init__(name, unit_price, stock, amount, final_price)
        self.Rows[0].append(self._supplier_element(supplier))
        self._add_percent_and_check_elements(percent, check)

    def _supplier_element(self, supplier):
        return Input(default_text=supplier,
                     size=SUPPLIER_ELEMENT_SIZE,
                     pad=SUPPLIER_ELEMENT_PAD)

    def buy_report(self):
        """
        :return: List[Fields]
        """
        return [
            self.get_name(), self.get_unit_price(), self.get_amount()
        ]


class Test:
    def __init__(self):
        index = [
            'Nombre', 'P/U', 'Stock', 'Cantidad', 'P/F', 'Proveedor', '%', 'Selec'
        ]
        index_elements = [
            [
                Input(i, readonly=True,
                      size=NAME_ELEMENT_SIZE,
                      pad=NAME_ELEMENT_PAD) for i in index
            ]
        ]
        layout = [
            [
                Button(button_text='test_report', border_width=BUTTON_BORDER_WIDTH),
                Button(button_text='test_is_empty', border_width=BUTTON_BORDER_WIDTH),
                Button(button_text='test_getters', border_width=BUTTON_BORDER_WIDTH),
                Button(button_text='test_buy_report', border_width=BUTTON_BORDER_WIDTH),
                Button(button_text='test_errors', border_width=BUTTON_BORDER_WIDTH),
            ], [
                Button(button_text='test_secure_mode', border_width=BUTTON_BORDER_WIDTH),
                Button(button_text='test_abble_to_sell', border_width=BUTTON_BORDER_WIDTH),
                Button(button_text='test_calculate_final_price', border_width=BUTTON_BORDER_WIDTH)
            ], [
                Button(button_text='test_apply_percent', border_width=BUTTON_BORDER_WIDTH),
                Button(button_text='test_update_from_sale_and_buy', border_width=BUTTON_BORDER_WIDTH),
                Button(button_text='test_update_from_report', border_width=BUTTON_BORDER_WIDTH),
            ], [
                Column(layout=index_elements)
            ], [
                SaleRecord('Nombre', 15.0, 25, 5, 0, 0, False)
                # BuyRecord('Nombre', 15.0, 25, 5, 0, 'Proveedor', 0, False)
                # StockRecord('Nombre', 15.0, 25, 0, False)
            ]
        ]
        self.win = Window(title='test', layout=layout)
        self.lt = layout[-1][0]
        self.run()

    def test_rows(self):
        print()
        print('ROWS')
        print(self.lt.Rows)
        print()

    def test_report(self):
        print()
        print('TEST_REPORT')
        print('report: ', self.lt.get_report())
        print('default_report: ', self.lt.get_default_report())
        print()

    def test_is_empty(self):
        print()
        print('TEST_IS_EMPTY')
        print('is_empty: ', self.lt.is_empty())
        print()

    def test_getters(self):
        print()
        print('TEST_GETTERS')
        print('name: ', self.lt.get_name(), type(self.lt.get_name()))
        print('unit_price: ', self.lt.get_unit_price(), type(self.lt.get_unit_price()))
        print('stock: ', self.lt.get_stock(), type(self.lt.get_stock()))
        print('amount: ', self.lt.get_amount(), type(self.lt.get_amount()))
        print('percent: ', self.lt.get_percent(), type(self.lt.get_percent()))
        print()

    def test_buy_report(self):
        print()
        print('test_buy_report')
        print(self.lt.buy_report())
        print()

    def test_secure_mode(self):
        print()
        print('TEST_SECURE_MODE')
        self.lt.secure_mode()
        print(StockRecord._secure_mode)
        print()

    def test_abble_to_sell(self):
        print()
        print('TEST_ABBLE_TO_SELL')
        print('Sale of -1: ', self.lt.abble_to_sell(-1))
        print('Sale of 25: ', self.lt.abble_to_sell(25))
        print('Sale of 26: ', self.lt.abble_to_sell(26))
        print()

    def test_update_from_sale_and_buy(self):
        print()
        print('TEST_UPDATE_FROM_SALE')
        self.lt.update_from_sale(-1)
        print('Sale of -1: ', self.lt.get_stock())
        self.lt.update_from_buy(15.0, - self.lt.get_stock())
        self.lt.update_from_buy(15.0, 25)
        self.lt.update_from_sale(25)
        print('Sale of 25: ', self.lt.get_stock())
        self.lt.update_from_buy(15.0, - self.lt.get_stock())
        self.lt.update_from_buy(15.0, 25)
        self.lt.update_from_sale(26)
        print('Sale of 26: ', self.lt.get_stock())
        print()

    def test_calculate_final_price(self):
        print()
        print('TEST_CALCULATE_FINAL_PRICE')
        self.lt.update_final_price(self.lt.calculate_final_price())
        print()

    def test_apply_percent(self):
        print()
        print('TEST_APPLY_PERCENT')
        self.lt.apply_percent()
        print()

    def test_update_from_report(self):
        print()
        print('TEST_UPDATE_FROM_REPORT')
        self.lt.update_from_report(['0', 0, 0, 0, True])
        print()

    def test_errors(self):
        print()
        print('TEST_ERRORS')
        error = self.lt.get_error_status()
        print('Error en: ', error)
        if error > -1:
            self.lt.indicate_error(error)
        else:
            self.lt.solve_error()
        print()

    def run(self):
        self.test_rows()
        while True:
            e, _ = self.win.read()
            if e == None:
                self.win.close()
                break
            getattr(self, e)()


if __name__ == '__main__':
    theme('PapelerAbasto')
    Test()
