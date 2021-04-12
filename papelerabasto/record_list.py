from tools import FileManager, Order, Searcher, Discarder, Index, Col


class RecordList(list):
    def __init__(self, name, order_by, discard_by, db_file, log_file, rc_class):
        """
        name: Referencia
        orderd_by: Ordenes por los que se rige la lista
        discard_by: Tipos de descarte de registros
        file: Nombre físico del archivo de carga
        """
        super().__init__(self)
        self._db_file = db_file
        self._log_file = log_file
        self.load(rc_class)
        self._order = Order(name, order_by)
        self._searcher = Searcher(name)
        self._discarder = Discarder(name, discard_by)

    def build(self, ls, size, index, sub_flieds) -> Col:
        ls_col = Col(ls, size=size, scrollable=True, vertical_scroll_only=True)
        fields = [
            [self._order.build()], [self._searcher.build(), self._discarder.build()], [Index.index(index)], [ls_col]
        ]
        fields += sub_flieds
        return Col(fields)

    def load(self, rc_class) -> None:
        """
        Carga los registros ubicados en el archivo
        """
        for rc in FileManager.load_of(self._db_file):
            _rc = [rc_class(rc)]
            self.append(_rc)

    def self_to_save(self) -> list:
        """
        Retorna una lista con los registros en formato string
        """
        rcs = []
        for rc in self:
            rcs.append(rc[0].self_to_save())
        return rcs

    def save(self) -> None:
        """
        Guarda los registros en el archivo
        """
        FileManager.save_of(self.self_to_save(), self._db_file)

    def search(self, name: str) -> list:
        for rc in self:
            if rc[0].name().upper() == name.upper():
                return rc
        return None

    def discard_rcs(self) -> bool:
        return getattr(self, self._discarder.discard_by())()

    def discard_selecteds(self) -> bool:
        have_discarded = False
        for rc in reversed(self):
                if rc[0].check():
                    self.remove(rc)
                    have_discarded = True
        return have_discarded

    def checks(self) -> list:
        checks = []
        for rc in self:
            if rc[0].check():
                checks.append(rc)
        return checks

    def search_in_window(self) -> None:
        name = self._searcher.get_in_search()
        if name:
            found = self.search(name)
            index = self.index(found)
            if found and index > 0:
                bu_found = found[0].self_to_save()
                for i in reversed(range(1, index+1)):
                    self[i][0].upd_all_fields(self[i-1][0].self_to_save())
                self[0][0].upd_all_fields(bu_found)

    def upd_all_rcs(self, new_rcs) -> None:
        for i in range(len(new_rcs)):
            self[i][0].upd_all_fields(new_rcs[i])
