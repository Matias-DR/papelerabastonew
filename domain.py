import constant as ct
import json
import os


class FileManager:
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
    def load(path):
        with open(path) as file:
            return json.load(file)


class Record:
    def __init__(self, fields):
        self._fields = fields

    def list(self):
        """
        Devuelve una lista con cada campo en string
        """
        return [
            str(field) for field in self._fields
        ]


class StockRecord:
    def __init__(self, fields):
        super().__init__(fields)


class SaleRecord:
    def __init__(self, fields):
        super().__init__(fields)


class BuyRecord:
    def __init__(self, fields):
        super().__init__(fields)


class ListControl:
    # """
    #     Clase y subclases con única instancia
    #     Define el control para la lista de registros
    # """
    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(ListControl, cls).__new__(cls)
    #     return cls.instance

    def __init__(self, path):
        self._path = path
        self._records = []

    def records(self):
        """
        [
            [ StockRecord() ],
            [ 0..* ]
        ]
        """
        return self._records

    def save(self):
        records = [
            record.list() for record in self._records
        ]
        FileManager.save_in_json(records, self._path)

    def add_records(self, records):
        for record in records:
            self._records.append(record)

    def del_records(self, records):
        for record in records:
            self._records.remove(record)

    def search(self, name):
        """
        Recibe un nombre y busca el registro con el mismo
        Devuelve su índice o -1 en caso de no existir
        """
        for i in range(len(self._records)):
            if self._records[i].name() == name:
                return i
        return False


class StockList(ListControl):
    def __init__(self):
        super().__init__('db/stock.json')
        self.load_records()

    def load_records(self):
        records = FileManager.load(self._path)
        for record in records:
            stock_record = [
                StockRecord(record)
            ]
            self._records.append(stock_record)


class SaleList(ListControl):
    def __init__(self):
        super().__init__('db/sales.json')
        self.load_records()

    def load_records(self):
        records = FileManager.load(self._path)
        for record in records:
            sale_record = [
                SaleRecord(record)
            ]
            self._records.append(sale_record)


class BuyList(ListControl):
    def __init__(self):
        super().__init__('db/buys.json')
        self.load_records()

    def load_records(self):
        records = FileManager.load(self._path)
        for record in records:
            buy_record = [
                BuyRecord(record)
            ]
            self._records.append(buy_record)
