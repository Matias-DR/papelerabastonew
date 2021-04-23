import constant as ct
import PySimpleGUI as ps
import json
import os
import csv


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
    _key = ''

    @classmethod
    def key(cls, key):
        cls._key = key

    def __init__(self, field_values, fields, readonly=None):
        name = ps.Input(default_text=field_values[0], pad=ct.NAME_INPUT_PAD,
                        size=ct.SIZES['m'], readonly=readonly)
        unit_price = ps.Input(default_text=field_values[1], pad=ct.MID_INPUT_PAD,
                              size=ct.SIZES['+s'], readonly=readonly)
        stock = ps.Input(default_text=field_values[2], pad=ct.MID_INPUT_PAD,
                         size=ct.SIZES['xs'], readonly=readonly)
        check = ps.Check('', default=field_values[-1], pad=ct.CHECK_PAD,
                               checkbox_color='White')
        self._fields = [
            name, unit_price, stock
        ]
        self._fields += fields
        self._fields.append(check)

    def fields(self):
        return self._fields

    def name(self):
        return self._fields[0].get()

    def percent(self):
        return self._fields[-2].get()

    def update(self, fields):
        for i, field in enumerate(fields):
            self._fields[i].update(field)

    def apply_percent(self):
        unit_price = self._fields[1]
        percent = self._fields[-2]
        new_price = round(float(unit_price.get()) + float(unit_price.get()) * float(percent.get()) / 100., 2)
        unit_price.update(new_price)
        percent.update(0)

    def selected(self):
        return self._fields[-1].get()


class StockRecord(Record):
    def __init__(self, field_values=ct.DEFAULT_STOCK_RC_VALUES):
        percent = ps.Spin(values=ct.SPIN_PERCENT_VALUES, initial_value=field_values[3],
                                readonly=True, pad=ct.PERCENT_PAD, size=ct.SIZES['xxs'])
        fields = [
            percent
        ]
        super().__init__(field_values, fields)

    def have_percent_to_apply(self):
        return bool(float(self._fields[3].get()))

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
        for field in self._fields[:-2]:
            field.update(disabled=ct.__secure__)


class SaleRecord(Record):
    """
    [ NAME, UNIT_PRICE, STOCK, AMOUNT, FINAL_PRICE, PERCENT, CHECK ]
    """
    _key = ''

    @classmethod
    def key(cls, key):
        cls._key = key

    def __init__(self, field_values, i):
        amount = ps.Input(default_text=field_values[3], enable_events=True, k=self._key+',amount',
                          pad=ct.MID_INPUT_PAD, size=ct.SIZES('xs'))
        final_price = ps.Input(default_text=field_values[4], pad=ct.SIZES('xs'),
                               readonly=True, size=ct.SIZES('xs'))
        percent = ps.Spin(values=ct.SPIN_PERCENT_VALUES, initial_value=field_values[-2],
                          pad=ct.PERCENT_PAD, size=ct.SIZES['xxs'], readonly=True,
                          enable_events=True, k=self._key+',apply_percent{}5'.format(i))
        fields = [
            amount, final_price, percent
        ]
        super().__init__(field_values, fields, True)

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

    def __init__(self, i, field_values=ct.DEFAULT_BUY_RC_VALUES):
        amount = ps.Input(default_text=field_values[3], enable_events=True, k=self._key+',amount{}5'.format(i),
                          pad=ct.MID_INPUT_PAD, size=ct.SIZES['xs'])
        final_price = ps.Input(default_text=field_values[4], pad=ct.MID_INPUT_PAD,
                               readonly=True, size=ct.SIZES['xs'])
        buyer = ps.Input(default_text=field_values[5], pad=ct.MID_INPUT_PAD, size=ct.SIZES['s'])
        percent = ps.Spin(values=ct.SPIN_PERCENT_VALUES, initial_value=field_values[6],
                          pad=ct.PERCENT_PAD, size=ct.SIZES['xxs'], readonly=True,
                          enable_events=True, k=self._key+',apply_percent{}6'.format(i))
        fields = [
            amount, final_price, buyer, percent
        ]
        super().__init__(field_values, fields)

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
            if record.name().upper() == name:
                return i
        return False

    def save(self):
        FileManager.save_in_json(self.report(), self._path)

    def clean_selected(self):
        for record in reversed(self._records):
            if record.selected():
                self._records.remove(record)
                ct.__restart__ = True


class StockList(ListControl):
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

    def records_to_apply_percent(self):
        return filter(lambda record: record.have_percent_to_apply(), self._records)

    def apply_percent(self):
        for record in self.records_to_apply_percent():
            record.apply_percent()

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


class SaleList(ListControl):
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


class BuyList(ListControl):
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
