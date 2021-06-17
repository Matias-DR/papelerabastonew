# # from random import choice

# # class A:
# #     def __init__(self):
# #         pass

# #     def pasar_lista(self):
# #         self._var = tuple(map(lambda _: choice([True, False]), range(5)))

# # class B(A):
# #     def __init__(self, ref=None):
# #         self._ref = ref
# #         self._var = None
# #         super().__init__()

# #     def var(self):
# #         return self._var

# #     def llega(self):
# #         print(self._ref._range)

# # class S:
# #     def __init__(self):
# #         self._range = 'Llega'
# #         for object, functions in tuple(
# #             map(
# #                 lambda object: (
# #                     object,
# #                     tuple(
# #                         filter(
# #                             lambda propiedad: propiedad.find('_'), dir(object)
# #                         )
# #                     )
# #                 ), (B(self), )
# #             )
# #         ):
# #             for function in functions:
# #                 setattr(self, function, getattr(object, function))

# #     def hola(self):
# #         print('hola')

# # clase = S()
# # print(tuple(filter(lambda propiedad: propiedad.find('_'), dir(clase))))
# # print(clase.pasar_lista())
# # print(clase.var())
# # print(clase.llega())
# # # print(tuple(map(lambda object: (object, object.dir()), (B(), ))))

# # def a(*p):
# #     print((p, ))
# #     print(type((p, )))

# # a(int, bool, float, list)

# class Config:
#     def setattr_in_object_from_objects(in_object, *from_objects):
#         for from_object in from_objects:
#             for function in dir(from_object):
#                 print('se evalua la funcion:', function, end=' ')
#                 if not function.startswith('_'):
#                     print('entra', end=' ')
#                     setattr(in_object, function, getattr(from_object, function))
#                 print()


# class Sorter:
#     class _Sorter:
#         def __init__(self):
#             pass

#     class _StrSorter(_Sorter):
#         def field(self, field):
#             return field

#     class _IntSorter(_Sorter):
#         def field(self, field):
#             try:
#                 return int(field)
#             except:
#                 return field

#     class _NOMBRE(_StrSorter):
#         ...

#     class _PU(_IntSorter):
#         ...

#     class _STOCK(_IntSorter):
#         ...

#     class _CANTIDAD(_IntSorter):
#         ...

#     class _PF(_IntSorter):
#         ...

#     class _PROVEEDOR(_StrSorter):
#         ...

#     def __init__(self, record_list):
#         self._record_list = record_list
#         self._index = self._NOMBRE()

#     def change_sorter(self):
#         self._index = getattr(
#             self,
#             '_' + Main.instance()[self.change_sorter].get()
#         )()

#     def _get_sort_index(self) -> int:
#         return cs.SORTER_COMBO_ALL_VALUES[Main.instance()[
#             self._record_list.change_sorter].get()]

#     def _sort(self, field_calc: callable, field: int, reverse: bool = False):
#         self._record_list._update_from_report(
#             sorted(
#                 self._record_list.get_report(),
#                 key=lambda rc: field_calc(rc[field]),
#                 reverse=reverse
#             )
#         )

#     def sort_list_min_max(self):
#         self._sort(self._index.field, self._get_sort_index())

#     def sort_list_max_min(self):
#         self._sort(self._index.field, self._get_sort_index(), True)


# class Remover:
#     class _Remover:
#         def __init__(self):
#             pass

#     class _SELECCIONADOS(_Remover):
#         def remove_records(self, rc_list) -> bool:
#             # return rc_list.remove_checked_records()
#             if rc_list._have_checked_records():
#                 for rc in reversed(rc_list.Rows):
#                     if rc[0].get_check():
#                         rc_list.Rows.remove(rc)
#                 rc_list.save_in_json()
#                 return True
#             return False

#     class _VACÍOS(_Remover):
#         def remove_records(self, rc_list) -> bool:
#             # return rc_list.remove_empty_records()
#             if rc_list.have_empty_records():
#                 for rc in reversed(rc_list.Rows):
#                     if rc[0].is_empty():
#                         rc_list.Rows.remove(rc)
#                 rc_list.save_in_json()
#                 return True
#             return False

#     class _TODOS(_Remover):
#         def remove_records(self, rc_list) -> bool:
#             # return rc_list.remove_all_records()
#             if rc_list.Rows:
#                 rc_list.Rows = []
#                 return True
#             return False

#     def __init__(self, record_list):
#         self._record_list = record_list
#         self._remover = self._SELECCIONADOS()

#     def change_remover(self):
#         self._remover = getattr(
#             self,
#             '_' + Main.instance()[self._record_list.change_remover].get()
#         )()

#     def remove_records(self) -> bool:
#         return self._remover.remove_records(self._record_list)



# class A:
#     def __init__(self):
#         print('esto es 2:', dir(self))

#     def __init_subclass__(self):
#         print('esto es 0:', dir(self))
#         Config.setattr_in_object_from_objects(self, Sorter(self), Remover(self))
#         print('esto es 1:', dir(self))
#         print('llega 1')

#     def sss(self):
#         pass

#     def __sss__(self):
#         pass


# class B(A):
#     def __init__(self):
#         print('llega 0')
#         super().__init__()


# class C:
#     def __init__(self):
#         Config.setattr_in_object_from_objects(self, B())


# c = C()
# print(dir(c))
# print(vars(c))
# # print(tuple(filter(lambda propiedad: not bool(propiedad.find('_') + 1), dir(B()))))

# ------------------------------
from PySimpleGUI import Window, Text, SaveAs

def export():
    print('entra')

layout = [
    [
        SaveAs(
            key=export,
            button_text='Export',
            file_types=(('', '.csv'), ),
            default_extension='.csv',
            target=(555666777, 0)
        ),
        Text(size=(20, 1))
    ]
]
win = Window(layout=layout)
while True:
    e, v = win.read()
    print(e, v)
    e()
# ------------------------------
