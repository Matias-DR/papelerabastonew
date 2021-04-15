from record_list import RecordList
from tools import FileManager, RecordAdder, FinalPrice, Col
from buy_record import BuyRecord
from PySimpleGUI import VerticalSeparator
from time import strftime


class BuyList(RecordList):
    _order_index = {
        'NOMBRE': 0, '$ UNI': 1, 'STOCK': 2, 'CANT.': 3, '$ FIN': 4, '±%': 5
    }

    def __init__(self, db_file, log_file, name='self._bsl'):
        self._record_adder = RecordAdder(name)
        self._final_price = FinalPrice(name, 'GENERAR COMPRA', 'buy')
        super().__init__(name, ['NOMBRE', '$ UNI', 'STOCK', 'CANT.', '$ FIN', 'COMPRADOR', '±%'],
                         {'VACÍOS': 'blanks', 'SELECCS.': 'selecteds', 'TODOS': 'all'},
                         db_file, log_file, BuyRecord)

    def order(self) -> bool:
        restart = False
        if self:
            restart = self.discard_blanks()
            order_key = lambda elem: elem[self._order_index[self._order.get_order_by()]]
            bu_self = sorted(self.self_to_save(), key=order_key,
                             reverse=True if self._order.get_order_way() == 'DE MAYOR A MENOR' else False)
            self.upd_all_rcs(bu_self)
        return restart

    def build(self, stl) -> Col:
        self._stl = stl
        index = {
            'NOMBRE': 'large', '$ UNI': 'short', 'CANT.': 'short',
            '$ FIN': 'short', 'PROVEEDOR': 'medium', '±%': 'very_short'
        }
        fields = [[self._record_adder.build(), VerticalSeparator(color='Black'), self._final_price.build()]]
        return super().build(self, (463, 146), index, fields)

    def discard_blanks(self) -> bool:
        have_discarded = False
        for rc in reversed(self):
            if rc[0].name() == '':
                self.remove(rc)
                have_discarded = True
        return have_discarded

    def discard_all(self) -> bool:
        have_discarded = False
        for rc in reversed(self):
            self.remove(rc)
            have_discarded = True
        return have_discarded

    def discard_buy(self, buy) -> None:
        for rc in reversed(buy):
            self.remove(rc)

    def add_new_rcs(self) -> True:
        """
        Agrega nuevos registros en blanco
        Requiere reinicio
        """
        for _ in range(self._record_adder.how_many_add()):
            self.append([BuyRecord()])
        return True

    def upd_prices(self) -> None:
        """
        Actualiza el precio de cada producto y el precio total
        """
        total_price = 0
        for rc in self:
            _rc = rc[0]
            price = _rc.upd_price()
            if _rc.deep_control():
                total_price += price
            elif _rc.name():            # Si hay campos vacíos menos el nombre
                existent_price = self._stl.search(_rc.name())[0].unit_price()           # Verificamos si existe el producto en stock
                _rc.upd_price(existent_price)           # Y actualizamos el producto en compra según su precio en stock
        self._final_price.upd_price(total_price)

    def register_buy(self, buys: list) -> None:
        _buy = 'Compra del {}. Total ${} - %{}\n'.format(strftime('%d/%m/%Y - %H:%M'),
                                                         self._final_price.price(),
                                                         self._final_price.literal_percent())
        for buy in buys:
            _buy += buy+'\n'
        FileManager.save_of_txt(_buy, self._log_file)

    def buy(self) -> bool:
        """
        Actualiza el stock según la compra
        Puede requerir reinicio
        """
        if self:
            self.upd_prices()
            buys = []
            buy_to_register = []
            for rc in reversed(self):
                _rc = rc[0]
                if _rc.deep_control(self._stl.search(_rc.name())):
                    buys.append(rc)
                    buy_to_register.append(_rc.self_to_register())
            if buys:
                self.register_buy(buy_to_register)
                self._stl.buy(buys)
                self.discard_buy(buys)
                return True
        return False
