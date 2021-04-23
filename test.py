# print(round(55.5 + 55.5 * 70. / 100., 2))


# class A:
#     def __init__(self):
#         self._var = 'casquito'
#         self._var_test = self._var_test2

#     def __str__(self):
#         """
#             También funciona.
#         """
#         return self._var_test

#     def var2(self):
#         """
#             Funciona. Linter marca un error por no encontrar la variable como local al objeto en el que se define el método.
#             Pero funciona y debería de implementar mis clases de esta manera.
#         """
#         print(self._var2)


# class B(A):
#     def __init__(self):
#         self._var_test2 = 'var_test2'
#         super().__init__()
#         self._var2 = 'casquito2'


# print(B())


import PySimpleGUI as ps
import constant as ct


ps.theme('PapelerAbasto')
layout = [
    [
        ps.In(key='input'), ps.B('', image_data=ct.PNG_SECURE_MODE(), key='btt')
    ]
]
win = ps.Window(title='', layout=layout)
while True:
    e, v = win.read()
    if e == 'btt':
        ct.__secure__ = not ct.__secure__
        win['input'].update(disabled=ct.__secure__)
        win['btt'].update(image_data=ct.PNG_SECURE_MODE())
    if e is None:
        win.close()
        break
