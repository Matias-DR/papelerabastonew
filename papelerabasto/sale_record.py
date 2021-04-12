from record import Record, In, Col
from tools import Sp


class SaleRecord(Record):
    _sp_range = [i for i in range(-100, 101, 5)]
    _index_percent = {
        -100: 0, -90: 0.1, -80: 0.2, -70: 0.3, -60: 0.4, -50: 0.5, -40: 0.6, -30: 0.7, -20: 0.8, -10: 0.9,
        0: 1, 10: 1.1, 20: 1.2, 30: 1.3, 40: 1.4, 50: 1.5, 60: 1.6, 70: 1.7, 80: 1.8, 90: 1.9, 100: 2,
        -95: 0.05, -85: 0.15, -75: 0.25, -65: 0.35, -55: 0.45, -45: 0.55, -35: 0.65, -25: 0.75, -15: 0.85, -5: 0.95,
        5: 1.05, 15: 1.15, 25: 1.25, 35: 1.35, 45: 1.45, 55: 1.55, 65: 1.65, 75: 1.75, 85: 1.85, 95: 1.95
    }

    def __init__(self, values=['', '', '', '', '', 0]):
        """
        values: ['NOMBRE', '$ UNI', 'STOCK', 'CANT', '$ FIN', '%', 'CHECK']
        *CHECK = 0 (True) or 1 (False)
        """
        super().__init__()
        self._default_values = values
        key='self._ssl,upd_prices,'+values[0]
        self._name = In(default_text=values[0], pad=self._pad, readonly=True,
                        border_width=self._bw, size=self._sizes['large'])
        self._unit_price = In(default_text=values[1], pad=self._pad, readonly=True,
                              border_width=self._bw, size=self._sizes['short'])
        self._stock = In(default_text=values[2], pad=self._pad, readonly=True,
                         border_width=self._bw, size=self._sizes['short'])
        self._amount = In(default_text=values[3], border_width=self._bw,
                          pad=self._pad, size=self._sizes['short'],
                          enable_events=True, k=key+',amount')
        self._final_price = In(default_text=values[4], pad=self._pad, readonly=True,
                               border_width=self._bw, size=self._sizes['short'])
        self._percent = Sp(self._sp_range, initial_value=values[5], pad=self._pad,
                           readonly=True, size=self._sizes['very_short'],
                           enable_events=True, k=key+',percent')
        self._fields += [self._name, self._unit_price, self._stock, self._amount,
                         self._final_price, self._percent, self._check]
        super().build()

    def self_to_save(self) -> list:
        """
        Retorna una lista con cada campo del registro
        Retorna la lista con cada campo vacío si no se levantó en pantalla
        -> ['NOMBRE', '$ UNI', 'STOCK', 'CANT', '$ FIN', '%']
        """
        try:
            return [element.get() for element in self._fields]
        except:
            return self._default_values

    def self_to_register(self) -> str:
        rc = ''
        for field in self._fields[:-1]:
            _field = str(field.get())
            if field == '':
                rc += ','+'1'
            else:
                rc += ','+_field
        return rc

    def is_empty(self) -> bool:
        try:
            for field in self._fields[:5]:
                if field.get():
                    return False
        except:
            for field in self._default_values[:5]:
                if field:
                    return False
        return True

    def is_complete(self) -> bool:
        for field in self._fields[:5]:
            if field.get() == '':
                return False
        return True

    def have_stock(self) -> bool:
        try:
            return (int(self._stock.get()) - int(self._amount.get())) > -1
        except:
            return False

    def amount(self) -> float:
        """
        Retorna la cantidad a vender
        Retorna 1 si no es una cantidad válida
        """
        try:
            return float(self._amount.get())
        except:
            self._amount.update(1)
            return 1

    def amount_control(self) -> float:
        amount = self._amount.get()
        try:
            amount = int(amount)
            stock = int(self._stock.get())
            if amount > stock:
                self._amount.update(stock)
                return float(stock)
            else:
                return float(amount)
        except:
            if amount == '':
                return 1
            self._amount.update(1)
            return 1

    def upd_price(self) -> float:
        """
        Actualiza y retorna el precio local
        """
        amount = self.amount_control()
        percent = self._index_percent[int(self._percent.get())]
        price = round(float(self._unit_price.get()) * amount * percent, 2)
        self._final_price.update(price)
        return price
