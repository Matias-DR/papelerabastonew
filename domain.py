import constant as ct
import PySimpleGUI as ps
import json
import os
import csv
import gui


class FileManager:
    @staticmethod
    def restart(location=None):
        if ct.OS == 'win32':
            os.system('python __init__.py')
        else:
            os.system('python3 __init__.py {} {}'.format(location[0], location[1]))

    @staticmethod
    def file_control():
        if not os.path.isdir('db'):
            os.mkdir('db')
            for path in ct.PATHS:
                with open(path, 'w') as file:
                    json.dump([], file)

    @staticmethod
    def save_in_json(data, path, mode='w'):
        with open(path, mode) as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def save_in_csv(data, path, mode='w'):
        with open(path, mode, newline='') as f:
            writer = csv.writer(f, delimiter=',', )
            for line in data:
                writer.writerow(line)

    @staticmethod
    def load(path):
        with open(path) as file:
            return json.load(file)


class Record:
    def __init__(self, field_values, readonly=None):
        name = ps.Input(default_text=field_values[0], pad=ct.NAME_INPUT_PAD,
                        size=ct.SIZES['l'], readonly=readonly)
        unit_price = ps.Input(default_text=field_values[1], pad=ct.MID_INPUT_PAD,
                              size=ct.SIZES['+s'], readonly=readonly)
        stock = ps.Input(default_text=field_values[2], pad=ct.MID_INPUT_PAD,
                         size=ct.SIZES['xs'], readonly=readonly)
        self._fields = [
            name, unit_price, stock
        ]
            # VER COMO SE GUARDA PRA QUE FUNCIONE EL BUY

    def add_check_field(self, value):
        check = ps.Check('', default=value, pad=ct.CHECK_PAD,
                               checkbox_color='White')
        self._fields.append(check)

    def add_comment_field(self, comment_field):
        self._fields.append(comment_field)

    def add_fields(self, fields):
        self._fields += fields

    def fields(self):
        return self._fields

    def name(self):
        return self._fields[0].get()

    def percent(self):
        return self._fields[-2].get()

    def update(self, fields):
        for i, field in enumerate(fields):
            self._fields[i].update(field)

    def selected(self):
        return self._fields[-1].get()

    def have_percent_to_apply(self):
        return bool(float(self._fields[-2].get()))


class StockRecord(Record):
    _key = ''

    @classmethod
    def key(cls, key):
        cls._key = key

    def __init__(self, field_values=ct.DEFAULT_STOCK_RC_VALUES):
        percent = ps.Spin(values=ct.SPIN_PERCENT_VALUES, initial_value=field_values[-2],
                          readonly=True, pad=ct.PERCENT_PAD, size=ct.SIZES['xxs'])
        fields = [
            percent
        ]
        super().__init__(field_values)
        self.add_fields(fields)
        self.add_check_field(field_values[-1])

    def csv_report(self):
        return [
            field.get() for field in self._fields
        ]

    def report(self):
        report = []
        try:
            for field in self._fields:
                report.append(field.get())
        except:
            report = ['', '', '', 0, 0]
        return report

    def secure_mode(self):
        for field in self._fields:
            field.update(disabled=ct.__secure__)

    def apply(self):
        unit_price = self._fields[1]
        percent = self._fields[-2]
        new_price = round(float(unit_price.get()) + float(unit_price.get()) * float(percent.get()) / 100., 2)
        unit_price.update(new_price)
        percent.update(0)

    def is_empty(self):
        return not bool(self._fields[0].get())

    def unit_price(self):
        try:
            return float(self._fields[1].get())
        except:
            return 0

    def amount(self):
        try:
            return int(self._fields[2].get())
        except:
            return 0

    def update_from_buy(self, unit_price, amount):
        self._fields[1].update(unit_price)
        self._fields[2].update(str(self.amount() + int(amount)))


class SaleRecord(Record):
    """
    [ NAME, UNIT_PRICE, STOCK, AMOUNT, FINAL_PRICE, PERCENT, CHECK ]
    """
    _key = ''

    @classmethod
    def key(cls, key):
        cls._key = key

    @classmethod
    def key(cls, key):
        cls._key = key

    def __init__(self, field_values, i):
        amount = ps.Input(default_text=field_values[3], enable_events=True, k=self._key+',amount,'+str(i),
                          pad=ct.MID_INPUT_PAD, size=ct.SIZES['xs'])
        final_price = ps.Input(default_text=field_values[4], pad=ct.MID_INPUT_PAD,
                               readonly=True, size=ct.SIZES['xs'])
        percent = ps.Spin(values=ct.SPIN_PERCENT_VALUES, initial_value=field_values[-2],
                          pad=ct.PERCENT_PAD, size=ct.SIZES['xxs'], readonly=True,
                          enable_events=True, k=self._key+',apply,'+str(i))
        fields = [
            amount, final_price, percent
        ]
        super().__init__(field_values, True)
        self.add_fields(fields)
        self.add_check_field(field_values[-2])

    def apply(self):
        unit_price = float(self._fields[1].get())
        amount = float(self._fields[3].get())
        percent = float(self._fields[-2].get())
        if percent == 0:
            percent = 1
        _price = round(unit_price * amount, 2)
        price = round(_price + _price * percent / 100., 2)
        self._fields[4].update(price)
        self._fields[-2].update(0)
        return price

    def csv_report(self):
        return [
            [
                'VENTA DEL '+ct.DATE+' A LAS '+ct.HOUR
            ],
            [
                field.get() for field in self._fields
            ]
        ]

    def report(self):
        report = []
        try:
            for field in self._fields:
                report.append(field.get())
        except:
            report = ['', '', '', '', '', 0, 0]
        return report


class BuyRecord(Record):
    """
    [ NAME, UNIT_PRICE, STOCK, AMOUNT, FINAL_PRICE, BUYER, PERCENT, CHECK ]
    """
    _key = ''

    @classmethod
    def key(cls, key):
        cls._key = key

    def __init__(self, i, field_values=ct.DEFAULT_BUY_RC_VALUES):
        amount = ps.Input(default_text=field_values[3], enable_events=True, k=self._key+',amount,'+str(i),
                          pad=ct.MID_INPUT_PAD, size=ct.SIZES['xs'])
        final_price = ps.Input(default_text=field_values[4], pad=ct.MID_INPUT_PAD,
                               readonly=True, size=ct.SIZES['xs'])
        buyer = ps.Input(default_text=field_values[5], pad=ct.MID_INPUT_PAD, size=ct.SIZES['s'])
        percent = ps.Spin(values=ct.SPIN_PERCENT_VALUES, initial_value=field_values[-2],
                          pad=ct.PERCENT_PAD, size=ct.SIZES['xxs'], readonly=True,
                          k=self._key+',apply,'+str(i))
        fields = [
            amount, final_price, buyer, percent
        ]
        super().__init__(field_values)
        self.add_fields(fields)
        self.add_check_field(field_values[-2])

    def csv_report(self):
        return [
            [
                'COMPRA DEL '+ct.DATE+' A LAS '+ct.HOUR
            ],
            [
                field.get() for field in self._fields
            ]
        ]

    def report(self):
        report = []
        try:
            for field in self._fields:
                report.append(field.get())
        except:
            report = ['', '', '','', '', '', 0, 0]
        return report

    def update_final_price(self, price):
        self._fields[4].update(price)
        self._fields[-2].update(0)

    def apply(self):
        unit_price = float(self._fields[1].get())
        amount = float(self._fields[3].get())
        percent = float(self._fields[-2].get())
        if percent == 0:
            percent = 1
        _price = round(unit_price * amount, 2)
        price = round(_price + _price * percent / 100., 2)
        self.update_final_price(price)
        return price

    def update_unit_price(self, unit_price):
        self._fields[1].update(unit_price)

    def buy_report(self):
        """
        [ NOMBRE, P/U, CANT. ]
        """
        return [
            self._fields[0].get(), self._fields[1].get(), self._fields[3].get()
        ]


class ListControl:
    def __init__(self):
        self._records = []

    def records(self):
        '''
        [
            Record 0..*
        ]
        '''
        return self._records

    def report(self):
        """
        [
            [ RECORD_DATA_FIELDS... ] 0..*
        ]
        """
        return [
            record.report() for record in self._records
        ]

    def sorted_report_min_max(self, index):
        return sorted(self.report(), key=lambda elem: elem[index])

    def sorted_report_max_min(self, index):
        return sorted(self.report(), key=lambda elem: elem[index], reverse=True)

    def search(self, name):
        for i, record in enumerate(self._records):
            if record.name().upper() == name.upper():
                return i
        return -1

    def record(self, name):
        index = self.search(name)
        if index > -1:
            return self._records[index]
        else:
            False

    def save(self):
        FileManager.save_in_json(self.report(), self._path)

    def clean_selected(self):
        for record in reversed(self._records):
            if record.selected():
                self._records.remove(record)
                ct.__restart__ = True

    def records_per_name(self):
        return [
            record.name() for record in self._records
        ]


class StockList(ListControl):
    _instance = None
    _key = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = StockList()
        return cls._instance

    @classmethod
    def key(cls, key):
        cls._key = key

    def __init__(self):
        super().__init__()
        self._path = 'db/stock.json'
        self.load_records()

    def load_records(self):
        '''
        [
            [ NAME, UNIT_PRICE, STOCK, CHECK, PERCENT ],
            [ 0..* ]
        ]
        '''
        records = FileManager.load(self._path)
        for record in records:
            self._records.append(StockRecord(record))

    def csv_report(self):
        return [
            record.report()[:3] for record in self._records
        ]

    def export(self, path):
        csv_report = [
            [
                'NOMBRE', 'PRECIO POR UNIDAD', 'STOCK'
            ]
        ]
        csv_report += self.csv_report()
        FileManager.save_in_csv(csv_report, path)

    def add_records(self, add):
        for _ in range(add):
            self._records.append(StockRecord())

    def records_to_apply(self):
        return filter(lambda record: record.have_percent_to_apply(), self._records)

    def apply(self):
        for record in self.records_to_apply():
            record.apply()

    def clean_empty(self):
        for record in reversed(self._records):
            if record.is_empty():
                ct.__restart__ = True
                self._records.remove(record)

    def collect(self, names):
        records = []
        for name in names:
            record = self.record(name)
            if record:
                records.append({'name': name, 'unit_price': record.unit_price()})
        return records

    def add_record_from_buy(self, record):
        record += [
            0, 0
        ]
        stock_record = StockRecord(record)
        layout = [
            stock_record.fields()
        ]
        window = gui.Main.window()
        window.extend_layout(window[self._key], layout)
        self._records.append(stock_record)

    def buy(self, records):
        for record in records:
            existent_record = self.record(record[0])
            if existent_record:
                existent_record.update_from_buy(record[1], record[2])
            else:
                ct.__restart__ = True
                self.add_record_from_buy(record)
            

class SaleList(ListControl):
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = SaleList()
        return cls._instance

    def __init__(self):
        super().__init__()
        self._path = 'db/sales.json'
        self.load_records()

    def load_records(self):
        '''
        [
            [ NAME, UNIT_PRICE, STOCK, CHECK, PERCENT, AMOUNT, FINAL_PRICE ],
            [ 0..* ]
        ]
        '''
        records = FileManager.load(self._path)
        for i, record in enumerate(records):
            self._records.append(SaleRecord(record, i))

    def csv_report(self):
        return [
            record.csv_report() for record in self._records
        ]

    def export(self, path):
        csv_report = [
            [
                'FECHA', 'NOMBRE', 'PRECIO POR UNIDAD', 'STOCK',
                'CANTIDAD A VENDER', 'PRECIO FINAL', 'PORCENTAJE'
            ]
        ]
        report = self.csv_report()
        if report:
            csv_report += report
            FileManager.save_in_csv(csv_report, path)

    def apply(self, percent):
        total = 0
        for record in self._records:
            try:
                total += record.apply()
            except:
                pass
        return round(total + total * percent / 100., 2)


class BuyList(ListControl):
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = BuyList()
        return cls._instance

    def __init__(self):
        super().__init__()
        self._path = 'db/buys.json'
        self.load_records()

    def load_records(self):
        '''
        [
            [ NAME, UNIT_PRICE, STOCK, CHECK, PERCENT, AMOUNT, FINAL_PRICE ],
            [ 0..* ]
        ]
        '''
        records = FileManager.load(self._path)
        for i, record in enumerate(records):
            self._records.append(BuyRecord(i, record))

    def csv_report(self):
        return [
            record.report()[:3] for record in self._records
        ]

    def export(self, path):
        csv_report = [
            [
                'FECHA', 'NOMBRE', 'PRECIO POR UNIDAD', 'STOCK',
                'CANTIDAD A VENDER', 'PRECIO FINAL', 'PORCENTAJE',
                'PROVEEDOR'
            ]
        ]
        report = self.csv_report()
        if report:
            csv_report += report
            FileManager.save_in_csv(csv_report, path)

    def add_records(self, add):
        for i in range(add):
            self._records.append(BuyRecord(i))

    def apply(self, percent):
        total = 0
        for record in self._records:
            try:
                total += record.apply()
            except:
                pass
        return round(total + total * percent / 100., 2)

    def collect(self):
        for record in StockList.instance().collect(self.records_per_name()):
            self.record(record['name']).update_unit_price(record['unit_price'])

    def buy_report(self):
        """
        [
            [ NOMBRE, P/U, CANT. ] 1..*
        ]
        """
        records = []
        for record in self._records:
            records.append(record.buy_report())
        return records

    def buy(self):
        StockList.instance().buy(self.buy_report())
        self._records = []

    def clean_all(self):
        self._records = []
        ct.__restart__ = True


if __name__ == '__main__':
    gui.Main((20, 20)).run()
