from record import Record, In, Col


class StockRecord(Record):
    def __init__(self, values=['', '', '', 0]):
        """
        values: ['NOMBRE', '$ UNI', 'STOCK', 'CHECK']
        *CHECK = 0 (True) or 1 (False)
        """
        super().__init__()
        self._default_values = values
        self._name = In(default_text=values[0], pad=self._pad,
                        border_width=self._bw, size=self._sizes['large'])
        self._unit_price = In(default_text=values[1], pad=self._pad,
                              border_width=self._bw, size=self._sizes['short'])
        self._stock = In(default_text=values[2], border_width=self._bw,
                         pad=self._pad, size=self._sizes['short'])
        self._fields += [self._name, self._unit_price, self._stock, self._check]
        super().build()

    def check(self) -> int:
        return self._check.get()

    def self_to_save(self) -> list:
        """
        Devuelve una lista con cada campo del registro
        Devuelve la lista con cada campo vacío si no se levantó en pantalla
        """
        try:
            return [element.get() for element in self._fields]
        except:
            return self._default_values

    def self_to_log(self) -> list:
        rc = ''
        for field in self._fields[:-1]:
            rc += field.get()+','
        return rc.strip(',')

    def self_to_sell(self) -> list:
        unit_price = self._unit_price.get()
        values = [self._name.get(), unit_price, self._stock.get()]
        values += [1, unit_price, 0]
        return values

    def decrease_stock(self, sold) -> None:
        self._stock.update(int(self._stock.get()) - sold)

    def is_empty(self) -> bool:
        try:
            for field in self._fields[:3]:
                if field.get():
                    return False
        except:
            for field in self._default_values[:3]:
                if field:
                    return False
        return True

    def have_stock(self) -> bool:
        try:
            return int(self._stock.get()) > 0
        except:
            return False

    def is_complete(self) -> bool:
        for field in self._fields[:3]:
            if field.get() == '':
                return False
        return True

    def char_control(self) -> bool:
        """
        Retorna True si los campos contienen caracteres
        válidos, False en caso contrario.
        """
        try:
            float(self._unit_price.get())
            int(self._stock.get())
            return True
        except:
            return False

    def deep_control(self) -> bool:
        """
        Verifica aptitud del registro.
        Control de completitud, stock y tipos de carácter por campo
        Retorna True en caso de ser apto, False en caso contrario
        """
        if self.is_complete():
            if self.char_control():
                return self.have_stock()
        return False

    def stock(self) -> int:
        try:
            return int(self._stock.get())
        except:
            return 0

    def upd_from_buy(self, buy) -> None:
        if float(buy.unit_price()) != 1:
            if float(self._unit_price.get()) != float(buy.unit_price()):
                self._unit_price.update(buy.unit_price())
        stock = self.stock()
        self._stock.update(stock + int(buy.amount()))

    def unit_price(self) -> float:
            try:
                return float(self._unit_price.get())
            except:
                return 1
