from record_list import RecordList
from stock_record import StockRecord
from tools import FileManager, RecordAdder, PreSell, B, Col, global_bd, theme_data
from PySimpleGUI import VerticalSeparator


class StockList(RecordList):
    _order_index = {
        'NOMBRE': 0, '$ UNI': 1, 'STOCK': 2
    }

    def __init__(self, db_file, log_file, name='self._stl'):
        self._name = name
        self._record_adder = RecordAdder(name)
        super().__init__(name, ['NOMBRE', '$ UNI', 'STOCK'], {'VACÍOS': 'blanks', 'SELECCS.': 'selecteds'},
                         db_file, log_file, StockRecord)

    def build(self, ssl, bsl) -> Col:
        """
        Recibe las referencias a la lista de ventas y la de compras
        """
        self._ssl = ssl
        self._bsl = bsl
        index = {'NOMBRE': 'large', '$ UNI': 'short', 'STOCK': 'short'}
        fields = [
            [
                self._record_adder.build(), VerticalSeparator(color='Black'),
                B('', border_width=global_bd, k=self._name+',pre_sell',
                  image_filename=theme_data['GENERAR PRE VENTA']),
                B('', k=self._name+',self_to_log', border_width=global_bd,
                  image_filename=theme_data['GUARDAR STOCK'])
            ]
        ]
        del self._name
        return super().build(self, (456, 350), index, fields)

    def self_to_log(self) -> None:
        rcs = 'NOMBRE, PRECIO POR UNIDAD, STOCK\n'
        for rc in self:
            rcs += rc[0].self_to_log()+'\n'
        FileManager.save_of_txt(rcs, self._log_file, 'w')
        print('LLEGUE')

    def order(self) -> bool:
        restart = False
        if self:
            restart = self.discard_blanks()
            order_key = lambda elem: elem[self._order_index[self._order.get_order_by()]]
            bu_self = sorted(self.self_to_save(), key=order_key,
                             reverse=True if self._order.get_order_way() == 'DE MAYOR A MENOR' else False)
            self.upd_all_rcs(bu_self)
        return restart

    def discard_blanks(self) -> bool:
        """
        Requiere reinicio si se descartan registros
        Puede requerir reinicio
        """
        have_discarded = False
        for rc in reversed(self):
            if rc[0].is_empty():
                self.remove(rc)
                have_discarded = True
        return have_discarded

    def add_new_rcs(self) -> True:
        """
        Agrega nuevos registros en blanco
        Requiere reinicio
        """
        for _ in range(self._record_adder.how_many_add()):
            self.append([StockRecord()])
        return True

    def add_new_rc(self, rc) -> None:
        self.append([StockRecord(rc.self_to_stock())])

    def pre_sell(self) -> bool:
        pre_sell = PreSell(self.checks())
        if not pre_sell.is_empty():
            return self._ssl.pre_sell(pre_sell)
        return False

    def sell(self, sold: dict) -> None:
        for name in sold:
            rc = self.search(name)
            rc[0].decrease_stock(sold[name])

    def buy(self, buys) -> None:
        for rc in buys:
            _rc = rc[0]
            found = self.search(_rc.name())
            if found:
                found[0].upd_from_buy(_rc)
            else:
                self.add_new_rc(_rc)
