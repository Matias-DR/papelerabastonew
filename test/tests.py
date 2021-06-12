import PySimpleGUI as ps


class Entry:
    def __init__(self):
        pass

    def update(self):
        Win.instance()['123'].update('Opciones:')


class Win(ps.Window):
    __instance = None

    @classmethod
    def instance(cls) -> ps.Window:
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self._entry = Entry()
        super().__init__(layout=self.render_layout())

    def render_layout(self):
        return [[ps.Input(key='123')], [ps.Button('Actualizar', key=self._entry.update)]]

    def run(self):
        print(self.__instance)
        while True:
            e, _ = self.read()
            if e == '__EXIT__':
                self.close()
                break
            e()


Win.instance().run()
