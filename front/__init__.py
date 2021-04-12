import constant as ct
import PySimpleGUI as ps


class ListComponent:
    def __init__(self, key, custom_discard_options):
        self._key = key
        self._sizes = {'xs': (5, 1), 's': (9, 1), 'sm': (11, 1), 'm': (14, 1), 'l': (21, 1), 'xl': (26, 1)}
        self._search_input = ps.Input(default_text='', key=self._key+',search_input',
                                      size=self._sizes['l'])
        discard_options = [
            'SELECCIONADOS'
        ]
        discard_options += custom_discard_options
        self._discard_options = ps.Combo(values=discard_options, default_value=discard_options[0],
                                 size=self._sizes['m'], key=self._key+',discard_options', readonly=True)
        self._index = {
            'NOMBRE': {'size': 'l', 'key': 'name'},
            '$ P/U': {'size': 's', 'key': 'unit_price'}
        }

    def build(self, index):
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
        return layout

    def index_field(self, field, key, size):
        return [
            [
                ps.Radio(text='', group_id=self._key, circle_color='White', pad=(0, 0), key=key)
            ], [
                ps.Input(default_text=field, readonly=True, pad=(0, 0), size=size)
            ]
        ]

    def index(self):
        layout = []
        for field in self._index:
            key = self._key+',sort_by_' + self._index[field]['key']
            size = self._sizes[self._index[field]['size']]
            layout.append(ps.Column(layout=self.index_field(field, key, size),
                                    pad=(0, 0), element_justification='center'))
        return layout

class StockListComponent(ListComponent):
    def __init__(self, key):
        custom_discard_options = [
            'VACIOS'
        ]
        super().__init__(key, custom_discard_options)

    def build(self):
        layout = super().build(self.index())
        del self._key
        del self._discard_options
        del self._index
        return layout

    def index(self):
        layout = super().index()
        key = self._key + ',sort_by_' + 'stock'
        size = self._sizes['s']
        index = self.index_field('STOCK', key, size)
        index[-1].append(ps.Button(button_text='', image_data=ct.PNG_APPLY, key=self._key+',refresh'))
        layout.append(ps.Column(layout=index, pad=(0, 0), element_justification='center'))
        return layout


class SalesListComponent(ListComponent):
    def __init__(self, key):
        custom_discard_options = [
            'TODOS'
        ]
        super().__init__(key, custom_discard_options)
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

    def build(self):
        layout = super().build(self.index())
        layout.append(self.total_price())
        del self._key
        del self._discard_options
        del self._index
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


class BuysListComponent(ListComponent):
    def __init__(self, key):
        custom_discard_options = [
            'TODOS'
        ]
        super().__init__(key, custom_discard_options)
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

    def build(self):
        layout = super().build(self.index())
        layout[0].append(ps.Button(button_text='', image_data=ct.PNG_REFRESH, key=self._key+',refresh'))
        layout.append(self.total_price())
        del self._key
        del self._discard_options
        del self._index
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


class Printer:
    def __init__(self, key):
        self._key = key
        self._file_name = ps.Input(default_text='', size=(50, 1), readonly=True)
        reports = [
            'InformeDeStock', 'InformeDeVentas', 'InformeDeCompras'
        ]
        self._reports = ps.Combo(values=reports, default_value=reports[0], size=(17, 1))
        self._initial_folder = str(__import__('pathlib').Path.home()) + '/' + reports[0] + '.csv'

    def build(self):
        layout = [
            [
                ps.FolderBrowse(button_text='', initial_folder=self._initial_folder,
                                target=(555666777, +1), image_data=ct.PNG_EXPORT,
                                key=self._key+',export'),
                self._file_name,
                self._reports
            ]
        ]
        del self._key
        del self._initial_folder
        return layout


class PapelerAbasto(ps.Window):
    def __init__(self):
        self._sk = StockListComponent(key='_sk')
        self._ss = SalesListComponent(key='_ss')
        self._bs = BuysListComponent(key='_bs')
        self._pr = Printer(key='_pr')
        ps.theme('PapelerAbasto')
        self._win = ps.Window(title='Papelera Abasto', layout=self.build(), font=24)

    def build(self):
        st_col = self._sk.build()
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
                ps.Column(layout=st_col),
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
            if event is None:
                self._win.close()
                break


if __name__ == '__main__':
    PapelerAbasto().run()
