class Record:
    def __init__(self):
        pass


class StockRecord:
    def __init__(self):
        pass


class SaleRecord:
    def __init__(self):
        pass


class BuyRecord:
    def __init__(self):
        pass


class ListControl(object):
    """
        Clase y subclases con única instancia
        Define el control para la lista de registros
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ListControl, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        pass


class StcokListControl(ListControl):
    def __init__(self):
        pass


class SaleListControl(ListControl):
    def __init__(self):
        pass


class BuyListControl(ListControl):
    def __init__(self):
        pass
