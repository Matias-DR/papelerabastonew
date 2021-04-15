from PySimpleGUI import Window, VerticalSeparator, HorizontalSeparator
from multiprocessing import Process
from stock_list import StockList
from sale_list import SaleList
from buy_list import BuyList
from tools import FileManager, Printer, Theme, B, Col, theme_data, global_bd, os
import sys


class PapeleraAbasto(Window):
    _db_files = ['./db/InformeDeStock.json', './db/InformeDeVentas.json', './db/InformeDeCompras.json']
    _log_files = ['./log/InformeDeStock.txt', './log/InformeDeVentas.txt', './log/InformeDeCompras.txt']

    def __init__(self, current_location):
        log_heads = {
            self._log_files[0]: 'NOMBRE, PRECIO POR UNIDAD, STOCK\n',
            self._log_files[1]: 'FECHA, NOMBRE, PRECIO POR UNIDAD, STOCK, CANTIDAD A VENDER, PRECIO FINAL, PORCENTAJE\n',
            self._log_files[2]: 'FECHA, NOMBRE, PRECIO POR UNIDAD, CANTIDAD A COMPRAR, PRECIO FINAL, PROVEEDOR, PORCENTAJE\n'
        }
        FileManager.check_files(self._db_files, self._log_files, log_heads)
        self._theme = Theme('self._theme')
        self._stl = StockList(self._db_files[0], self._log_files[0])
        self._ssl = SaleList(self._db_files[1], self._log_files[1])
        self._bsl = BuyList(self._db_files[2], self._log_files[2])
        self._ls = [self._stl, self._ssl, self._bsl]
        self._printer = Printer()
        self.build(current_location)
        self._clock = 0
        self.run()

    def build(self, current_location) -> None:
        layout_theme_update = [
            [self._theme.build()],
            [B('', k='upd', border_width=global_bd, image_filename=theme_data['ACTUALIZAR'])]
        ]
        col_theme_update = Col(layout_theme_update)
        layout_stock_printer = [
            [self._stl.build(self._ssl, self._bsl)],
            [HorizontalSeparator(color='Black')],
            [
                self._printer.build('self._printer'),
                VerticalSeparator(color='Black'),
                col_theme_update,
            ]
        ]
        col_stock_printer = Col(layout_stock_printer)
        layout_sales_build = [
            [self._ssl.build(self._stl)], [HorizontalSeparator(color='Black')], [self._bsl.build(self._stl)]
        ]
        col_sales_build = Col(layout_sales_build)
        layout = [[col_stock_printer, VerticalSeparator(color='Black'), col_sales_build]]
        super().__init__('Papelera Abasto', layout, return_keyboard_events=True,
                         element_padding=(1, 1), margins=(1, 1), finalize=True,
                         location=current_location, border_depth= 0)
        self._ssl.upd_prices()
        self._bsl.upd_prices()

    def run(self) -> None:
        while True:
            event, _ = self.read(timeout=1000)
            self.clock()
            print(event)
            try:
                event_split = event.split(',')
                var, func = (event_split[0], event_split[1])
                if getattr(eval(var), func)():
                    self.restart()
            except:
                try:
                    if event is None:
                        self._stl.self_to_save()
                        self.close(save_all=True)
                    if event == 'F5:116' or event == 'F5:71':
                        self.restart()
                    if event == 'upd':
                        self.upd()
                except:
                    exit()

    def clock(self):
        if self._clock == 120:
            self._clock = 0
            self.bu(False)
        else:
            self._clock += 1

    def bu(self, restart=None):
        self._stl.self_to_log()
        self.save_all()
        if restart:
            Process(target=os.system, args=('./upd.sh', )).start()
        else:
            Process(target=os.system, args=('./upd.sh {}'.format(restart), )).start()

    def upd(self):
        self._stl.self_to_log()
        self._stl.save()
        super().close()
        Process(target=os.system, args=('./upd.sh', )).start()
        exit()

    def close(self, timeout=0, save_all=False) -> None:
        if save_all:
            self.save_all()
        self.read(timeout=timeout)
        super().close()
        os.system('./bu.sh')
        exit()

    def restart(self) -> None:
        """
        save: Recibe una lista con las listas a guardar
        """
        self.save_all()
        Process(target=FileManager.restart, args=(self.current_location(), )).start()
        self.close(timeout=1000)

    def save_all(self) -> None:
        for l in self._ls:
            l.save()

    def save(self, *save) -> None:
        for l in save:
            l.save()


if __name__ == '__main__':
    try:
        location = (int(sys.argv[-2])-2, int(sys.argv[-1])-30)
    except:
        location = (0, 0)
    PapeleraAbasto(location)
