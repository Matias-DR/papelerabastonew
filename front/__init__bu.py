import constant as ct
import PySimpleGUI as ps
import json as js
import os
import sys
from multiprocessing import Process


class Record(ps.Column):
    # USAR __REPR__ Y/O __ADD__ PARA -REPRESENTAR- AL OBJETO REGISTRO MEDIANTE STRING O LA LISTA
    def __init__(self, key, default_values):
        """
        default_values = [name, unit_price, stock, percent]
        """
        self._key = key
        self._name = ps.Input(default_text=default_values[0])
        self._unit_price = ps.Input(default_text=default_values[1])
        self._stock = ps.Input(default_text=default_values[2])
        self._percent = ps.Spin(values=ct.SPIN_PERCENT_VALUES, initial_value=default_values[3],
                                readonly=True, size=ct.SIZES['xs'],
                                enable_events=True, k=self._key+',percent')
        self._fields = [
            self._name, self._unit_price, self._stock
        ]

    def build(self):
        return [
            [
                super.__init__(Layout=[self._fields])
            ]
        ]

    def self_to_save(self):
        data_fields = []
        for field in self._fields:
            data_field = field.get()
            data_fields.append(data_field)
        return data_fields


class StockRecord(Record):
    def __init__(self, key, default_values):
        super().__init__(key, default_values)

    def build(self):
        self._fields.append(self._percent)
        return super().build()


class SaleRecord(Record):
    def __init__(self, key, default_values):
        """
        default_values = [name, unit_price, stock, percent, amount, total_price]
        """
        super().__init__(key, default_values)
        self._amount = ps.Input(default_text=default_values[4])
        self._total_price = ps.Input(default_text=default_values[5])

    def build(self):
        self._fields.append(self._amount)
        self._fields.append(self._total_price)
        self._fields.append(self._percent)
        return super().build()


class BuyRecord(Record):
    def __init__(self, key, default_values):
        """
        default_values = [name, unit_price, stock, percent, amount, total_price, supplier]
        """
        super().__init__(key, default_values)
        self._amount = ps.Input(default_text=default_values[4])
        self._total_price = ps.Input(default_text=default_values[5])
        self._supplier = ps.Input(default_text=default_values[6])

    def build(self):
        self._fields.append(self._amount)
        self._fields.append(self._total_price)
        self._fields.append(self._supplier)
        self._fields.append(self._percent)
        return super().build()


class ListComponent:
    def __init__(self, key):
        self._records = []
        try:
            self.load()
        except:
            pass
        self._key = key
        self._search_input = ps.Input(default_text='', key=self._key+',search_input',
                                      size=ct.SIZES['l'])
        self._index = {
            'NOMBRE': {'size': 'l', 'key': 'name'},
            '$ P/U': {'size': 's', 'key': 'unit_price'}
        }
        self._funcs = {}

    def build(self, index, custom_discard_options):
        discard_options = [
            'SELECCIONADOS'
        ]
        discard_options += custom_discard_options
        self._discard_options = ps.Combo(values=discard_options, default_value=discard_options[0],
                                         size=ct.SIZES['m'], key=self._key+',discard_options', readonly=True)
        layout = [
            [
                self._search_input,
                ps.Button(button_text='', image_data=ct.PNG_SEARCH, key=self._key+',search'),
                ps.Button(button_text='', image_data=ct.PNG_SORT_MIN_TO_MAX, key=self._key+',sort_min_to_max'),
                ps.Button(button_text='', image_data=ct.PNG_SORT_MAX_TO_MIN, key=self._key+',sort_max_to_min'),
                self._discard_options,
                ps.Button(button_text='', image_data=ct.PNG_DELETE, key=self._key+',discard')
            ], index
        ]
        self.render_records(layout)
        return layout

    def render_index_field(self, field, key, size):
        return [
            [
                ps.Radio(text='', group_id=self._key, circle_color='White', pad=(0, 0), key=key)
            ], [
                ps.Input(default_text=field, readonly=True, pad=(0, 0), size=size)
            ]
        ]

    def render_index(self):
        layout = []
        for field in self._index:
            key = self._key+',sort_by_' + self._index[field]['key']
            size = ct.SIZES[self._index[field]['size']]
            index_field = self.render_index_field(field, key, size)
            layout.append(ps.Column(layout=index_field, pad=(0, 0), element_justification='center'))
        return layout

    def render_records(self, layout):
        records = [
            self._records
        ]
        record_list = [
            ps.Col(layout=records, scrollable=True, vertical_scroll_only=True)
        ]
        layout.append(record_list)

    def callback(self, func):
        return self._funcs[func]()

    def records_to_save(self):
        records = []
        for record in self._records:
            record_to_save = record.self_to_save()
            records.append(record_to_save)
        return records

    def save(self):
        with open('records.json', 'w') as file:
            js.dump(self.records_to_save(), file, indent=4)

    def load(self, func):
        with open('records.json') as file:
            records = js.load(file)
        func(records)

class StockListComponent(ListComponent):
    def __init__(self, key):
        super().__init__(key)
        funcs = {
            'add_records': self.add_records
        }
        self._funcs.update(funcs)
        self._spin_record_adder = ps.Spin(values=ct.SPIN_RECORD_ADDER_VALUES, initial_value=0)

    def funcs(self):
        return {}

    def build(self):
        custom_discard_options = [
            'VACIOS'
        ]
        index = self.render_index()
        layout = super().build(index, custom_discard_options)
        # del self._key
        del self._discard_options
        del self._index
        self._funcs.update(self.funcs())
        return layout

    def render_record_adder(self, layout):
        layout[-1].append(ps.Button(button_text='', image_data=ct.PNG_ADD, key=self._key+',add_records'))
        layout[-1].append(self._spin_record_adder)

    def render_button_apply(self, layout):
        layout[-1].append(ps.Button(button_text='', image_data=ct.PNG_APPLY, key=self._key+',apply'))

    def render_last_index_field(self):
        key = self._key + ',sort_by_' + 'stock'
        size = ct.SIZES['s']
        last_index_field = self.render_index_field('STOCK', key, size)
        return last_index_field

    def render_index(self):
        index = super().render_index()
        last_index_field = self.render_last_index_field()
        self.render_button_apply(last_index_field)
        self.render_record_adder(last_index_field)
        index.append(ps.Column(layout=last_index_field, pad=(0, 0), element_justification='center'))
        return index

    def add_records(self):
        """
            -> Restart: Restart = (True | False)
        """
        records_to_add = self._spin_record_adder.get()
        if records_to_add > 0:
            for i in range(records_to_add):
                self._records.append(StockRecord(self._key, ['', '', '', '']))
            self.save()
            return True
        return False

    def records_from_load(self, records):
        for record in records:
            self._records.append(StockRecord(self._key, record))

    def load(self):
        super().load(self.records_from_load)


class SalesListComponent(ListComponent):
    def __init__(self, key):
        super().__init__(key)
        funcs = {
        }
        self._funcs.update(funcs)
        self._index.update({
                            'STOCK': {
                                'size': 's', 'key': 'stock'
                            },
                            'CANTIDAD': {
                                'size': 's', 'key': 'amount'
                            },
                            '$ FIN': {
                                'size': 's', 'key': 'final_price'
                            }
                           })

    def funcs(self):
        return {}

    def build(self):
        custom_discard_options = [
            'TODOS'
        ]
        layout = super().build(self.render_index(), custom_discard_options)
        layout.append(self.total_price())
        del self._key
        del self._discard_options
        del self._index
        self._funcs.update(self.funcs())
        return layout

    def total_price(self):
        return [
            ps.Button(button_text='', image_data=ct.PNG_CART_ACCEPT, key=self._key+',accept_sell'),
            ps.Button(button_text='', image_data=ct.PNG_CART_CANCEL, key=self._key+',cancel_sell'),
            ps.Text(text='$0000.00', key=self._key+',total_price',
                    background_color='White', text_color='Black'),
            ps.Spin([i for i in range(-100, 101, 5)], initial_value=0, size=(4, 1),
                    enable_events=True, readonly=True, k=self._key+',upd_prices')
        ]

    def records_from_load(self, records):
        for record in records:
            self._records.append(SaleRecord(self._key, record))

    def load(self):
        super().load(self.records_from_load)


class BuysListComponent(ListComponent):
    def __init__(self, key):
        super().__init__(key)
        funcs = {
        }
        self._funcs.update(funcs)
        self._index.update({
                            'STOCK': {
                                'size': 's', 'key': 'stock'
                            },
                            'CANTIDAD': {
                                'size': 's', 'key': 'amount'
                            }, 'PROVEEDOR': {
                                'size': 'sm', 'key': 'percent'
                            }, '$ FIN': {
                                'size': 's', 'key': 'final_price'
                            }
                           })

    def funcs(self):
        return {}

    def build(self):
        custom_discard_options = [
            'TODOS'
        ]
        layout = super().build(self.render_index(), custom_discard_options)
        layout[0].append(ps.Button(button_text='', image_data=ct.PNG_REFRESH, key=self._key+',refresh'))
        layout.append(self.total_price())
        del self._key
        del self._discard_options
        del self._index
        self._funcs.update(self.funcs())
        return layout

    def total_price(self):
        return [
            ps.Button(button_text='', image_data=ct.PNG_CART_ACCEPT, key=self._key+',accept_buy'),
            ps.Button(button_text='', image_data=ct.PNG_CART_CANCEL, key=self._key+',cancel_buy'),
            ps.Text(text='$0000.00', key=self._key+',total_price',
                    background_color='White', text_color='Black'),
            ps.Spin([i for i in range(-100, 101, 5)], initial_value=0, size=(3, 1),
                    enable_events=True, readonly=True, k=self._key+',upd_prices')
        ]

    def records_from_load(self, records):
        for record in records:
            self._records.append(BuyRecord(self._key, record))

    def load(self):
        super().load(self.records_from_load)


class Printer:
    def __init__(self, key):
        self._key = key
        self._file_name = ps.Input(default_text='', size=(50, 1), readonly=True)
        self._initial_folder = str(__import__('pathlib').Path.home()) + '/' + 'InformeDeStock' + '.csv'
        self._funcs = {
        }

    def funcs(self):
        return {}

    def build(self):
        reports = [
            'InformeDeStock', 'InformeDeVentas', 'InformeDeCompras'
        ]
        self._reports = ps.Combo(values=reports, default_value=reports[0], size=(17, 1))
        layout = [
            [
                ps.Button(button_text='', image_data=ct.PNG_DOWNLOAD, key=self._key+',export'),
                ps.FolderBrowse(button_text='', initial_folder=self._initial_folder,
                                target=(555666777, +1), image_data=ct.PNG_EXPORT),
                self._file_name,
                self._reports
            ]
        ]
        del self._key
        del self._initial_folder
        self._funcs.update(self.funcs())
        return layout

    def callback(self, func):
        return self._funcs[func]()


class PapelerAbasto:
    def __init__(self):
        self._sk = StockListComponent(key='self._sk')
        self._ss = SalesListComponent(key='self._ss')
        self._bs = BuysListComponent(key='self._bs')
        self._pr = Printer(key='self._pr')
        ps.theme('PapelerAbasto')
        self._win = ps.Window(title='Papelera Abasto', layout=self.build(), font=24)

    def build(self):
        ss_bs_col = [
            [
                ps.Column(layout=self._ss.build())
            ], [
                ps.HorizontalSeparator(color='Black')
            ], [
                ps.Column(layout=self._bs.build())
            ]
        ]
        return [
            [
                ps.Column(layout=self._sk.build()),
                ps.VerticalSeparator(color='Black'),
                ps.Column(layout=ss_bs_col)
            ], [
                ps.HorizontalSeparator(color='Black')
            ], [
                ps.Column(layout=self._pr.build())
            ]
        ]

    def run(self):
        while True:
            event, _ = self._win.read()
            try:
                splitted_event = event.split(',')
                var = splitted_event[0]
                func = splitted_event[1]
                # print('event: ', event)
                if getattr(eval(var), 'callback')(func):
                    self.restart()
            except:
                pass
            if event is None:
                self._win.close()
                break

    def restart(self):
        if sys.platform == 'win32':
            restart = 'python d:/Documentos/Trabajo/papelerabasto/front/papelerabasto-gui/__init__.py'
        else:
            restart = 'python3 d:/Documentos/Trabajo/papelerabasto/front/papelerabasto-gui/__init__.py'
        Process(target=os.system, args=(restart, )).start()
        self._win.read(timeout=1000)
        self._win.close()
        exit()


if __name__ == '__main__':
    PapelerAbasto().run()
    """
    ------------------------------- COMENTARIOS -------------------------------
    - HAY QUE HACER REFACTOR
    """