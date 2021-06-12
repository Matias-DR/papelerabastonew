import unittest
from record import *
from record_list import *


class TestRecord():
    def __init__(self):
        theme('PapelerAbasto')
        index = [
            'Nombre', 'P/U', 'Stock', 'Cantidad', 'P/F', 'Proveedor', '%',
            'Selec'
        ]
        index_elements = [
            [
                Input(i, readonly=True, size=NAME_SIZE, pad=NAME_PAD)
                for i in index
            ]
        ]
        layout = [
            [
                Button(
                    button_text='test_report',
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text='test_buy_report',
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text='test_errors',
                    button_color=('White', 'Green'),
                    key='test_errors'
                ),
                Button(
                    button_text='test_secure_mode',
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text='test_abble_to_sell',
                    button_color=('White', 'Green')
                )
            ],
            [
                Button(
                    button_text='test_apply_percent',
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text='test_update_from_report',
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text='test_stock_control',
                    button_color=('White', 'Green')
                )
            ],
            [
                Button(
                    button_text='test_buy',
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text='test_calculate_final_price',
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text='test_sale',
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text='test_sale_report',
                    button_color=('White', 'Green')
                )
            ], [Column(layout=index_elements)],
            [StockRecord('Nombre', 15.0, 25, 0, False)],
            [SaleRecord('Nombre', 15.0, 25, 5, 0, 0, False)],
            [BuyRecord('Nombre', 15.0, 25, 5, 0, 'Proveedor', 0, False)]
        ]
        self.win = Window(title='test', layout=layout)
        self.lt = (layout[-3][0], layout[-2][0], layout[-1][0])
        print()
        print('test_rows')
        self.test_rows()
        while True:
            e, _ = self.win.read()
            if e == None:
                self.win.close()
                break
            print()
            print(e)
            getattr(self, e)()

    def test_rows(self):  # OK
        print(self.lt[0]._get_fields())
        print(self.lt[1]._get_fields())
        print(self.lt[2]._get_fields())

    def test_report(self):  # OK
        print(self.lt[0].get_report())
        print(self.lt[1].get_report())
        print(self.lt[2].get_report())

    def test_buy_report(self):  # OK
        print(self.lt[2].get_buy_report())

    def test_sale_report(self):  # OK
        print(self.lt[1].get_sale_report())

    def test_secure_mode(self):  # OK
        self.lt[0].change_secure_mode()
        self.lt[0].secure_mode()
        print(StockRecord._secure_mode)

    def test_abble_to_sell(self):  # OK
        print('Sale of 0: ', self.lt[0].able_to_sell(0))
        print('Sale of 25: ', self.lt[0].able_to_sell(25))
        print('Sale of 26: ', self.lt[0].able_to_sell(26))

    def test_errors(self):  # OK
        self.lt[0].clear_issues()
        self.lt[1].clear_issues()
        self.lt[2].clear_issues()
        self.lt[0].passes_control()
        self.lt[1].passes_control()
        self.lt[2].passes_control()

    def test_sale(self):  # OK
        amount = self.lt[1].get_amount()
        if self.lt[0].able_to_sell(amount):
            self.lt[0].update_from_sale(amount)

    def test_buy(self):  # OK
        self.lt[0].update_from_buy(
            self.lt[2].get_unit_price(), self.lt[2].get_amount()
        )

    def test_calculate_final_price(self):  # OK
        self.lt[1].clear_issues()
        self.lt[2].clear_issues()
        if self.lt[1].passes_control():
            self.lt[1].apply_final_price()
        if self.lt[2].passes_control_for_calculate_final_price():
            self.lt[2].apply_final_price()

    def test_apply_percent(self):  # OK
        self.lt[0].apply_percent()

    def test_update_from_report(self):  # OK
        self.lt[0].update_from_report(('Nombre', 35.0, 50, 0, True))

    def test_stock_control(self):  # OK
        self.lt[0].clear_issues()
        self.lt[0].passes_stock_control()


class TestRecordList():
    def __init__(self):
        FileManager.db_control()
        layout = [
            [
                Button(
                    button_text="test_add_records",
                    key="test_add_records",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_sell_records",
                    key="test_sell_records",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_stock_control",
                    key="test_stock_control",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_remove_empty_records",
                    key="test_remove_empty_records",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_instance",
                    key="test_instance",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_secure_mode",
                    key="test_secure_mode",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_uncheck_records",
                    key="test_uncheck_records",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_export",
                    key="test_export",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_collect_prices",
                    key="test_collect_prices",
                    button_color=('White', 'Green')
                ),
            ],
            [
                Button(
                    button_text="test_apply_percent",
                    key="test_apply_percent",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_sort_min_max",
                    key="test_sort_min_max",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_sort_max_min",
                    key="test_sort_max_min",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_remove_checked_records",
                    key="test_remove_checked_records",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_csv_report",
                    key="test_csv_report",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_sell",
                    key="test_sell",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_buy",
                    key="test_buy",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_pre_sell",
                    key="test_pre_sell",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_pre_buy",
                    key="test_pre_buy",
                    button_color=('White', 'Green')
                ),
                Button(
                    button_text="test_check_all",
                    key="test_check_all",
                    button_color=('White', 'Green')
                )
            ],
            [StockList.instance(),
             SaleList.instance(),
             BuyList.instance()],
        ]
        self.win = Window(
            title="test", layout=layout, enable_close_attempted_event=True
        )
        self.lt = layout[-1]
        print()
        print('test_rows')
        self.test_rows()
        while True:
            e, _ = self.win.read()
            if e == "-WINDOW CLOSE ATTEMPTED-":
                self.save()
                self.close()
                break
            print()
            print(e)
            list_lens = (
                self.lt[0].get_records_len(), self.lt[1].get_records_len(),
                self.lt[2].get_records_len()
            )
            getattr(self, e)()
            if list_lens != (
                self.lt[0].get_records_len(), self.lt[1].get_records_len(),
                self.lt[2].get_records_len()
            ):
                self.restart()

    def test_apply_percent(self):  # OK
        self.lt[0].apply_percent_to_records()

    def test_uncheck_records(self):  # OK
        self.lt[0].uncheck_records()
        self.lt[1].uncheck_records()
        self.lt[2].uncheck_records()

    def test_remove_empty_records(self):  # OK
        self.lt[0].remove_empty_records()
        self.lt[2].remove_empty_records()

    def test_instance(self):  # OK
        print(self.lt[0] == StockList.instance())
        print(self.lt[1] == SaleList.instance())
        print(self.lt[2] == BuyList.instance())

    def test_rows(self):  # OK
        print(self.lt[0].Rows)
        print(self.lt[1].Rows)
        print(self.lt[2].Rows)

    def test_collect_prices(self):  # OK
        self.lt[2].collect_unit_prices()

    def test_export(self):  # OK
        self.lt[0].export("./st.csv")
        self.lt[1].export("./ss.csv")
        self.lt[2].export("./bs.csv")

    def test_csv_report(self):  # OK
        print(self.lt[0].get_csv_report())
        print(self.lt[1].get_csv_report())
        print(self.lt[2].get_csv_report())

    def test_sell(self):  # OK
        self.lt[1].sell_records()

    def test_buy(self):  # OK
        self.lt[2].buy_records()

    def test_pre_sell(self):  # OK
        self.lt[0].pre_sell()

    def test_pre_buy(self):  # OK
        self.lt[0].pre_buy()

    def test_add_records(self):  # OK
        lt0 = self.lt[0].get_records_len()
        lt2 = self.lt[2].get_records_len()
        self.lt[0].add_records(1)
        self.lt[2].add_records(1)
        self.assertTrue(self.lt[0].get_records_len() > lt0)
        self.assertTrue(self.lt[2].get_records_len() > lt2)

    def test_remove_checked_records(self):  # OK
        self.lt[0].remove_checked_records()
        self.lt[1].remove_checked_records()
        self.lt[2].remove_checked_records()

    def test_sort_min_max(self):  # OK
        self.lt[0].sort_list_min_max(0)
        self.lt[1].sort_list_min_max(0)
        self.lt[2].sort_list_min_max(0)

    def test_sort_max_min(self):  # OK
        self.lt[0].sort_list_max_min(0)
        self.lt[1].sort_list_max_min(0)
        self.lt[2].sort_list_max_min(0)

    def test_check_all(self):  # OK
        self.lt[0].check_all()
        self.lt[1].check_all()
        self.lt[2].check_all()

    def test_secure_mode(self):  # OK
        self.lt[0].secure_mode()

    def test_stock_control(self):  # OK
        self.lt[0].passes_stock_control()

    def save(self):
        for lt in self.lt:
            lt.save_in_json()

    def close(self, timeout=0):
        self.win.read(timeout=timeout, close=True)
        exit()

    def restart(self):
        Process(
            target=FileManager.restart, args=(self.win.current_location(), )
        ).start()
        self.close(1000)


if __name__ == '__main__':
    # TestRecord()
    TestRecordList()
