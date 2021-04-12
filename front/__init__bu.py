import constant as ct
import PySimpleGUI as ps


class ListComponent:
    def __init__(self, key):
        self._key = key
        self._sizes = {'xs': (5, 1), 's': (9, 1), 'sm': (11, 1), 'm': (14, 1), 'l': (21, 1), 'xl': (26, 1)}
        self._search_input = ps.Input(default_text='', key=self._key+',search_input',
                                      size=self._sizes['l'])
        self._discard_options = [
            'SELECCIONADOS'
        ]
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
                ps.Combo(values=self._discard_options, default_value='SELECCIONADOS',
                         size=self._sizes['m'], key=self._key+',discard_options'),
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

class StockListComponent(ListComponent):
    def __init__(self, key):
        super().__init__(key)
        self._discard_options.append('VACIOS')

    def build(self):
        layout = super().build(self.index())
        layout[-1].append(ps.Button(button_text='', key=self._key+',apply',
                          image_data=ct.PNG_APPLY, image_size=(43, 43)))
        del self._key
        del self._discard_options
        del self._index
        return layout

# 'STOCK': {
#                                 'size': 's', 'key': 'stock'
#                             },

    def index(self):
        layout = []
        for field in self._index:
            key = self._key+',sort_by_' + self._index[field]['key']
            size = self._sizes[self._index[field]['size']]
            layout.append(ps.Column(layout=self.index_field(field, key, size), pad=(0, 0)))
        
        return layout


class SalesListComponent(ListComponent):
    def __init__(self, key):
        super().__init__(key)
        self._discard_options.append('TODOS')
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
        del self._key
        del self._discard_options
        del self._index
        return layout

    def index(self):
        layout = []
        for field in self._index:
            key = self._key+',sort_by_' + self._index[field]['key']
            size = self._sizes[self._index[field]['size']]
            layout.append(ps.Column(layout=self.index_field(field, key, size), pad=(0, 0)))
        return layout


class BuysListComponent(ListComponent):
    def __init__(self, key):
        super().__init__(key)
        self._discard_options.append('TODOS')
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
        del self._key
        del self._discard_options
        del self._index
        return layout

    def index(self):
        layout = []
        for field in self._index:
            key = self._key+',sort_by_' + self._index[field]['key']
            size = self._sizes[self._index[field]['size']]
            layout.append(ps.Column(layout=self.index_field(field, key, size), pad=(0, 0)))
        return layout


class PapelerAbasto(ps.Window):
    def __init__(self):
        self._sk = StockListComponent(key='_sk')
        self._ss = SalesListComponent(key='_ss')
        self._bs = BuysListComponent(key='_bs')
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
