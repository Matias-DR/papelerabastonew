from record_list import RecordList
from tools import FileManager, Index, FinalPrice, Col
from sale_record import SaleRecord
from time import strftime


class SaleList(RecordList):
    _order_index = {
        'NOMBRE': 0, '$ UNI': 1, 'STOCK': 2, 'CANT.': 3, '$ FIN': 4, '±%': 5
    }

    def __init__(self, db_file, log_file, name='self._ssl'):
        self._final_price = FinalPrice(name, 'GENERAR VENTA', 'sell')
        super().__init__(name, ['NOMBRE', '$ UNI', 'STOCK', 'CANT.', '$ FIN', '±%'],
                         {'SELECCS.': 'selecteds', 'TODOS': 'all'}, db_file, log_file, SaleRecord)

    def build(self, stl) -> Col:
        self._stl = stl
        index = {
            'NOMBRE': 'large', '$ UNI': 'short', 'STOCK': 'short',
            'CANT.': 'short', '$ FIN': 'short', '±%': 'very_short'
        }
        fields = [[self._final_price.build()]]
        return super().build(self, (463, 146), index, fields)

    def order(self) -> None:
        if self:
            order_key = lambda elem: elem[self._order_index[self._order.get_order_by()]]
            bu_self = sorted(self.self_to_save(), key=order_key,
                             reverse=True if self._order.get_order_way() == 'DE MAYOR A MENOR' else False)
            self.upd_all_rcs(bu_self)

    def upd_prices(self) -> None:
        """
        Actualiza el precio de cada producto y el precio total
        """
        total_price = 0
        for rc in self:
            total_price += rc[0].upd_price()
        self._final_price.upd_price(total_price)

    def discard_all(self) -> bool:
        have_discarded = False
        for rc in reversed(self):
            self.remove(rc)
            have_discarded = True
        return have_discarded

    def discard_sold(self, sold_to_discard: list) -> None:
        for rc in reversed(sold_to_discard):
            self.remove(rc)

    def pre_sell(self, pre_sell) -> True:
        """
        Crea los registros de venta desde la preventa
        Requiere reinicio
        """
        self.clear()
        for product in pre_sell.pre_sell():
            self.append([SaleRecord(product)])
        return True

    def register_sale(self, sold: list) -> None:
        _sale = 'Venta del {}. Total ${} - %{}\n'.format(strftime('%d/%m/%Y - %H:%M'),
                                                         self._final_price.price(),
                                                         self._final_price.literal_percent())
        for sale in sold:
            _sale += sale+'\n'
        FileManager.save_of_txt(_sale, self._log_file)

    def sell(self) -> bool:
        """
        Actualiza el stock según la venta
        Puede requerir reinicio
        """
        if self:
            self.upd_prices()
            sold = {}
            sold_to_discard = []
            sale = []
            for rc in reversed(self):
                _rc = rc[0]
                if _rc.have_stock():
                    sale.append(_rc.self_to_register())
                    sold.update({_rc.name(): int(_rc.amount())})
                    sold_to_discard.append(rc)
            if sale:
                self.register_sale(sale)
                self._stl.sell(sold)
                self.discard_sold(sold_to_discard)
                return True
        return False
