from record import Record, In, Col
from tools import Sp


class BuyRecord(Record):
    _sp_range = [i for i in range(-100, 101, 5)]
    _index_percent = {
        -100: 0, -90: 0.1, -80: 0.2, -70: 0.3, -60: 0.4, -50: 0.5, -40: 0.6, -30: 0.7, -20: 0.8, -10: 0.9,
        0: 1, 10: 1.1, 20: 1.2, 30: 1.3, 40: 1.4, 50: 1.5, 60: 1.6, 70: 1.7, 80: 1.8, 90: 1.9, 100: 2,
        -95: 0.05, -85: 0.15, -75: 0.25, -65: 0.35, -55: 0.45, -45: 0.55, -35: 0.65, -25: 0.75, -15: 0.85, -5: 0.95,
        5: 1.05, 15: 1.15, 25: 1.25, 35: 1.35, 45: 1.45, 55: 1.55, 65: 1.65, 75: 1.75, 85: 1.85, 95: 1.95
    }

    def __init__(self, values=['', '', '', '', '', 0, 0]):
        """
        values: ['NOMBRE', '$ UNI', 'CANT', '$ FIN', 'COMPRADOR', '%', 'CHECK']
        *CHECK = 0 (True) or 1 (False)
        """
        super().__init__()
        self._default_values = values
        key='self._bsl,upd_prices,'+values[0]
        self._name = In(default_text=values[0], pad=self._pad,
                        border_width=self._bw, size=self._sizes['large'])
        self._unit_price = In(default_text=values[1], pad=self._pad,
                              border_width=self._bw, size=self._sizes['short'],
                              enable_events=True, k=key+',unit_price')
        self._amount = In(default_text=values[2], border_width=self._bw,
                          pad=self._pad, size=self._sizes['short'],
                          enable_events=True, k=key+',amount')
        self._final_price = In(default_text=values[3], pad=self._pad, readonly=True,
                               border_width=self._bw, size=self._sizes['short'])
        self._buyer = In(default_text=values[4], border_width=self._bw,
                         pad=self._pad, size=self._sizes['medium'])
        self._percent = Sp(self._sp_range, initial_value=values[5], pad=self._pad,
                           readonly=True, size=self._sizes['very_short'],
                           enable_events=True, k=key+',percent')
        self._fields += [self._name, self._unit_price, self._amount, self._final_price,
                         self._buyer, self._percent, self._check]
        super().build()

    def self_to_save(self) -> list:
        """
        Devuelve una lista con cada campo del registro
        Devuelve la lista con cada campo vacío si no se levantó en pantalla
        """
        try:
            return [element.get() for element in self._fields]
        except:
            return self._default_values

    def self_to_stock(self) -> list:
        """
        -> ['NOMBRE', '$ UNI', 'STOCK', 'CHECK']
        *CHECK = 0 (False)
        """
        return [self.name(), self.unit_price(), int(self.amount()), 0]

    def self_to_register(self) -> str:
        rc = ''
        for field in self._fields[:-1]:
            rc += ','+str(field.get())
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

    def is_complete(self, found) -> bool:
        is_complete = True
        if not found:
            for field in self._fields[:5]:
                if field.get() == '':
                    is_complete =  False
        else:
            if self._fields[0].get() == '':
                is_complete = False
            else:
                for field in self._fields[2:5]:
                    if field.get() == '':
                        is_complete =  False
        return is_complete

    def char_control(self, found) -> bool:
        try:
            if not found:
                float(self._unit_price.get())
            int(self._amount.get())
            return True
        except:
            return False

    def deep_control(self, found=False) -> bool:
        """
        Verifica aptitud del registro.
        Control de completitud y tipos de carácter por campo
        Retorna True en caso de ser apto, False en caso contrario
        """
        if self.is_complete(found):
            return self.char_control(found)

    def amount(self) -> float:
        try:
            return float(self._amount.get())
        except:
            return 1

    def unit_price(self) -> float:
        try:
            return float(self._unit_price.get())
        except:
            return 1

    def upd_price(self, existent_price=None) -> float:
        """
        Actualiza y retorna el precio local
        """
        if existent_price:
            unit_price = existent_price
            self._unit_price.update(unit_price)
        else:
            unit_price = self.unit_price()
        amount = self.amount()
        percent = self._index_percent[int(self._percent.get())]
        price = round(amount * percent * unit_price, 2)
        self._final_price.update(price)
        return price
