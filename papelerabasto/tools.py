from PySimpleGUI import B, FolderBrowse, T, Drop, In, Sp, Check, Col, HorizontalSeparator, theme
import json as js
import os
import csv


# GLOBALS
global_bd = 0
theme_data = {}
def set_theme_data(data):
    theme_data.update(data)


class FileManager:
    @staticmethod
    def restart(curr_loc) -> None:
        os.system('python3 papelerabasto.py {} {}'.format(curr_loc[0], curr_loc[1]))

    @staticmethod
    def save_of_txt(data, file, mode='a') -> None:
        with open(file, mode) as f:
            f.write(data)

    @staticmethod
    def check_files(db_files: list, log_files: list, heads: dict) -> None:
        if not os.path.isdir('./db'):
            os.mkdir('./db')
            for file in db_files:
                with open(file, 'w') as f:
                    js.dump([], f)
        if not os.path.isdir('./log'):
            os.mkdir('./log')
            for file in log_files:
                FileManager.save_of_txt(heads[file], file, mode='w')
        if not os.path.isdir('./themes'):
            os.mkdir('./themes')
            FileManager.save_of('CUSTOM_PAPELERABASTO_DARK', './themes/theme.json')

    @staticmethod
    def load_of_txt(file):
        with open(file) as f:
            return f.read()

    @staticmethod
    def load_of(file):
        with open(file) as f:
            return js.load(f)

    @staticmethod
    def save_of(data, file, mode='w') -> None:
        with open(file, mode) as f:
            js.dump(data, f, indent=4)

    @staticmethod
    def load_screen_size() -> tuple:
        try:
            with open('./json/screen_size.json') as f:
                return js.load(f)
        except FileNotFoundError:
            user32 = __import__('ctypes').windll.user32
            monitor_resolution = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
            with open('./json/screen_size.json', 'w') as f:
                js.dump(monitor_resolution, f)
            return monitor_resolution

    @staticmethod
    def save_of_csv(data, file, mode='a'):
        with open(file, mode, newline='') as f:
            writer = csv.writer(f, delimiter=',', )
            for line in data:
                writer.writerow(line)


class Theme:
    @staticmethod
    def set_theme(folder):
        data = {
            'AGREGAR': folder+'agregar.png',
            'BUSCAR': folder+'buscar.png',
            'DESCARTAR': folder+'descartar.png',
            'EN': folder+'en.png',
            'EXPORTAR': folder+'exportar.png',
            'GENERAR COMPRA': folder+'generar_compra.png',
            'GENERAR PRE VENTA': folder+'generar_pre_venta.png',
            'GENERAR VENTA': folder+'generar_venta.png',
            'GUARDAR STOCK': folder+'guardar_stock.png',
            'ORDENAR POR': folder+'ordenar_por.png',
            'CAMBIAR TEMA': folder+'cambiar_tema.png',
            'ACTUALIZAR': folder+'actualizar.png'
        }
        set_theme_data(data)

    @staticmethod
    def CUSTOM_PAPELERABASTO_DARK():
        Theme.set_theme('./themes/dark/')

    @staticmethod
    def CUSTOM_PAPELERABASTO_LIGHT():
        Theme.set_theme('./themes/light/')

    def __init__(self, name):
        self._file = './themes/theme.json'
        self._theme = self.theme_load()
        theme(self._theme)
        getattr(Theme, self._theme)()
        self._theme_button = B('', border_width=global_bd,k=name+',switch_theme',
                               image_filename=theme_data['CAMBIAR TEMA'])

    def theme_load(self):
        return FileManager.load_of(self._file)

    def build(self):
        return self._theme_button

    def switch_theme(self) -> True:
        if self._theme == 'CUSTOM_PAPELERABASTO_DARK':
            FileManager.save_of('CUSTOM_PAPELERABASTO_LIGHT', self._file)
        else:
            FileManager.save_of('CUSTOM_PAPELERABASTO_DARK', self._file)
        return True


class PreSell:
    def __init__(self, pre_sell):
        """
        Recibe una lista de registros seleccionados para su venta
        """
        self._pre_sell = pre_sell
        self.control()

    def control(self) -> None:
        """
        Verifica y elimina cada registro que no esté completo,
        o no contenga stock, o se encuentre repetido.
        """
        duplicate_control = []
        for check in reversed(self._pre_sell):
            rc = check[0]
            if rc.name().upper in duplicate_control or not rc.deep_control():
                self._pre_sell.remove(check)
            else:
                duplicate_control.append(rc.name().upper())

    def is_empty(self) -> bool:
        return False if self._pre_sell else True

    def pre_sell(self) -> list:
        """
        Retorna los registros en formato de pre venta:
        [['NOMBRE', '$ UNI', 'STOCK', 'CANT.', '$ FIN', '%'], ...]
        """
        return [pre_sell[0].self_to_sell() for pre_sell in self._pre_sell]


class FinalPrice:
    _index_percent = {
        -100: 0, -90: 0.1, -80: 0.2, -70: 0.3, -60: 0.4, -50: 0.5, -40: 0.6, -30: 0.7, -20: 0.8, -10: 0.9,
        0: 1, 10: 1.1, 20: 1.2, 30: 1.3, 40: 1.4, 50: 1.5, 60: 1.6, 70: 1.7, 80: 1.8, 90: 1.9, 100: 2,
        -95: 0.05, -85: 0.15, -75: 0.25, -65: 0.35, -55: 0.45, -45: 0.55, -35: 0.65, -25: 0.75, -15: 0.85, -5: 0.95,
        5: 1.05, 15: 1.15, 25: 1.25, 35: 1.35, 45: 1.45, 55: 1.55, 65: 1.65, 75: 1.75, 85: 1.85, 95: 1.95
    }

    def __init__(self, name, event, k):
        self._final_price = T('0000.00', pad=(0, 0), size=(7, 1),
                              border_width=1, k=name+',final_price')
        self._final_percent = Sp([i for i in range(-100, 101, 5)], initial_value=0, size=(3, 1),
                                 enable_events=True, readonly=True, k=name+',upd_prices')
        self._final_event = B('', border_width=global_bd, k=name+','+k,
                              image_filename=theme_data[event])

    def build(self) -> Col:
        layout = [[T('$'), self._final_price, self._final_percent, self._final_event]]
        return Col(layout)

    def percent(self) -> float:
        return self._index_percent[self._final_percent.get()]

    def literal_percent(self) -> int:
        return self._final_percent.get()

    def upd_price(self, final_price: float) -> None:
        final_price = round(final_price * self._index_percent[int(self._final_percent.get())], 2)
        self._final_price.update(final_price)

    def price(self) -> float:
        return self._final_price.get()


class RecordAdder:
    def __init__(self, name):
        self._add_new_rcs = B('', k=name+',add_new_rcs', border_width=global_bd,
                              image_filename=theme_data['AGREGAR'])
        self._how_many_add = Sp(values=[i for i in range(0, 21, 2)], size=(3, 1),
                                initial_value=1, readonly=10, k=name+',how_many_add')

    def build(self) -> Col:
        layout = [[self._add_new_rcs, self._how_many_add, T('REGISTROS')]]
        return Col(layout)

    def how_many_add(self) -> int:
        return int(self._how_many_add.get())


class Order:
    _generic_pad = (0, 0)
    _generic_b_w = 1
    _drop_size = (22, 1)

    def __init__(self, name, order_by):
        self._order = B('', k=name+',order', border_width=global_bd,
                        image_filename=theme_data['ORDENAR POR'])
        self._order_by = Drop(order_by, size=self._drop_size, default_value=order_by[0], 
                              enable_events=True, readonly=True, k=name+',order_by')
        self._order_way = Drop(['DE MENOR A MAYOR', 'DE MAYOR A MENOR'], readonly=True, enable_events=True,
                               default_value='DE MENOR A MAYOR', size=self._drop_size, k=name+',order_way')

    def build(self) -> Col:
        layout = [[self._order, self._order_by, self._order_way]]
        return Col(layout)

    def get_order_by(self) -> str:
        return self._order_by.get()

    def get_order_way(self) -> str:
        return self._order_way.get()


class Searcher:
    def __init__(self, name):
        self._search = B('', k=name+',search_in_window', border_width=global_bd,
                         image_filename=theme_data['BUSCAR'])
        self._in_search = In('', size=(20, 1), border_width=1, pad=(0, 0), k=name+',in_search')

    def build(self) -> Col:
        layout = [[self._search, self._in_search]]
        return Col(layout)

    def get_in_search(self) -> str:
        return self._in_search.get()


class Discarder:
    _drop_size = (9, 1)

    def __init__(self, name, discard_by):
        self._discard_by_index = discard_by
        discard_by_keys = list(discard_by.keys())
        self._discard_rcs = B('', k=name+',discard_rcs', border_width=global_bd,
                              image_filename=theme_data['DESCARTAR'])
        self._discard_by = Drop(discard_by_keys, default_value=discard_by_keys[0], readonly=True, 
                                size=self._drop_size, k=name+',discard_by')

    def build(self) -> Col:
        layout = [[self._discard_rcs, self._discard_by]]
        return Col(layout)

    def discard_by(self) -> str:
        return 'discard_'+self._discard_by_index[self._discard_by.get()]


class Index:
    @staticmethod
    def index(index) -> Col:
        sizes = {'very_short': (4, 1), 'short': (7, 1), 'medium': (12, 1), 'large': (20, 1)}
        _index = [[In(i, readonly=True, size=sizes[index[i]], pad=(0, 0), border_width=1) for i in index]]
        return Col(_index)


class Printer:
    def __init__(self):
        self._files = {
            'STOCK': 'InformeDeStock',
            'VENTAS': 'InformeDeVentas',
            'COMPRAS': 'InformeDeCompras'
        }
        self._format_files = {'TEXTO': 'txt', 'EXCEL': 'csv'}
        self._default_dir = '/home/papelerabasto/Desktop/'

    def build(self, name):
        drop_size = {'short': (7, 1), 'medium': (10, 1)}
        export = B('', k=name+',print_file', border_width=global_bd,
                   image_filename=theme_data['EXPORTAR'])
        ls_values = ['STOCK', 'VENTAS', 'COMPRAS']
        self._ls = Drop(ls_values, ls_values[0], size=drop_size['medium'], readonly=True)
        text_01 = T('FORMATO')
        formats_values = ['TEXTO', 'EXCEL']
        self._formats = Drop(formats_values, formats_values[1], size=drop_size['short'], readonly=True)
        folder_browser = FolderBrowse('', initial_folder='/home/papelerabasto/Desktop/', border_width=global_bd,
                                      target=(555666777, +1), image_filename=theme_data['EN'])
        self._dir = In(default_text=self._default_dir, size=(36, 1), readonly=True)
        layout = [[export, self._ls, text_01, self._formats], [folder_browser, self._dir]]
        return Col(layout)

    def print_txt(self, data, file):
        file += '.txt'
        FileManager.save_of_txt(data, file, 'w')

    def print_csv(self, data, file):
        file += '.csv'
        data = data.split('\n')
        for i in range(len(data)):
            data[i] = data[i].split(',')
        FileManager.save_of_csv(data, file, 'w')

    def get_dir(self):
        file = self._files[self._ls.get()]
        custom_dir = self._dir.get()
        if custom_dir[-1] == '/' or custom_dir[-1] == '\\':
            custom_dir = custom_dir+file
        else:
            custom_dir = custom_dir+'/'+file
        return custom_dir

    def print_file(self) -> None:
        data = FileManager.load_of_txt('./log/'+self._files[self._ls.get()]+'.txt')
        if data:
            getattr(self, 'print_'+self._format_files[self._formats.get()])(data, self.get_dir())