from tools import In, Check, Col


class Record(Col):
    _sizes = {'very_short': (4, 1), 'short': (7, 1), 'medium': (12, 1), 'large': (20, 1)}
    _pad = (0, 0)
    _bw = 1

    def __init__(self):
        """
        values: ['NOMBRE', '$ UNI' ...]
        """
        self._check = Check('')
        self._fields = []

    def name(self) -> str:
        return self._fields[0].get()

    def check(self) -> int:
        return self._check.get()

    def build(self) -> None:
        fields = [self._fields]
        super().__init__(layout=fields, pad=self._pad)

    def values(self) -> list:
        return [value.get() for value in self._fields]

    def upd_all_fields(self, new_fields) -> None:
        for i in range(len(new_fields)):
            self._fields[i].update(new_fields[i])
