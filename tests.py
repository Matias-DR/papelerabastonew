# import PySimpleGUI as ps

# # class Rc(ps.Col):
# #     def __init__(self, key):
# #         super().__init__([[ps.B('ok')]], key=key, scrollable=True, vertical_scroll_only=True, size=(400, 350))

# # rcs_col = ps.Col([[ps.Check('check')]], key='col')
# col = ps.Col([[ps.Check('check')]], key='col')
# # col = Rc(key='col')
# col.AddRow(ps.In('nada'), ps.B('ok'))
# layout = [
#     [
#         col
#     ]
# ]
# win = ps.Window('test', layout=layout)
# while True:
#     e, _ = win.read()
#     if e == None:
#         win.close()
#         break
#     if e == 'ok':
#         it = iter([1, 2, 3])
#         print(*it)
#         col.AddRow(ps.Check('...'))
#         # print(col.Rows)
#         print(col.Rows[-1][0].InitialState)
#         # win.extend_layout(col, [[ps.In('asd')]])

# class A:
#     _v: str

#     def __init__(self):
#         pass

#     def a(self):
#         print('class A')

# class B(A):
#     def __init__(self):
#         B._v = 'BB'

#     def b(self):
#         print('class B')

# class S:
#     def __init__(self):
#         self.un = 'una var'

#     def pr(self):
#         print('esto es', self, 'con', self.un)

# class C(A, S):
#     def __init__(self):
#         super(A, self).__init__()
#         super(S, self).__init__()
#         C._v = 'CC'

#     def c(self):
#         self.a()

# C().pr()

# from time import perf_counter
# ES MAS RAPIDA LA TUPLA QUE LA LISTA
# a = 0
# for i in range(999):
#     b = perf_counter()
#     sum((1, 2, 3, 4, 5, 6, 7, 8, 9))
#     a += perf_counter() - b
# print('con tupla: ', a/999)

# a = 0
# for i in range(999):
#     b = perf_counter()
#     sum([1, 2, 3, 4, 5, 6, 7, 8, 9])
#     a += perf_counter() - b
# print('con lista: ', a/999)

# def lam(elem, index):
#     try:
#         print('puede', elem[index])
#     except:
#         return elem

# l = [[1], [2]]

# st = set(map(lam, range(len(l)), l))
# for i, elem in enumerate(st):
#     st.pop(i)

# from random import randint as ri

# CSV_HEADER = (
#     (
#         'DATE()', 'TIME()'
#     )
# )
# CSV_STOCK_HEADER = CSV_HEADER, (
#     (
#         'NOMBRE', 'PRECIO POR UNIDAD', 'STOCK'
#     )
# )

# def rep(data):
#     return (ri(1, 10), ri(1, 10))

# print(CSV_STOCK_HEADER + tuple(map(rep, (1, 2, 3))))

# try:
#     print(float('sa'))
# except:
#     pass
# finally:
#     print('fic')

# print(tuple(map(lambda elem: elem[0], [[1], [2], [3]])))

# from random import randint as ri

# def hex(a):
#     return (ri(1, 10), ri(1, 10))

# print(list(map(hex, range(3))))

# l1 = (1, 2, 3)
# l2 = (5, 2, 3)

# print(list(set(l1).intersection(set(l2))))



# from PySimpleGUI import theme, Window, Frame, Column, Radio, Input, Button, FileSaveAs

# theme('Default1')
# radio_pad = ((0, 0), (0, 0))
# radio_size = (0, 0)
# input_pad = ((0, 0), (0, 0))
# column_pad = ((0, 0), (0, 0))
# l1 = [
#     [
#         Radio(
#             text='',
#             group_id=0,
#             pad=radio_pad,
#             size=radio_size,
#             background_color='Grey'
#         )
#     ], [Input(default_text='first_index', pad=input_pad)]
# ]
# l2 = [[Column(element_justification='center', layout=[
#     [
#         Radio(
#             # text='',
#             group_id=0,
#             pad=radio_pad,
#             size=radio_size,
#             background_color='Grey'
#         )
#     ], [Input(default_text='second_index', pad=input_pad, size=(25, 1))],
#     [FileSaveAs(enable_events=True, key='save_as')]
# ])]]



# layout2 = [
#     [
#         Column(
#             layout=l1,
#             background_color='Grey',
#             element_justification='center',
#             pad=column_pad
#         ),
#         Button('hola')
#     ]
# ]
# layout1 = [
#     [
#         Frame(
#             title='a_frame',
#             layout=[
#                 [
#                     Column(
#                         layout=l2,
#                         background_color='Grey',
#                         element_justification='center',
#                         pad=column_pad,
#                         key='col'
#                     )
#                 ]
#             ]
#         ),
#         Radio(
#             text='',
#             group_id=1,
#             key='key1',
#             pad=radio_pad,
#             size=radio_size,
#             background_color='Grey'
#         ),
#         Radio(
#             text='',
#             group_id=1,
#             key='key2',
#             pad=radio_pad,
#             size=radio_size,
#             background_color='Grey'
#         )
#     ]
# ]
# layout = layout1 + layout2



# win = Window(title='PapelerAbasto', layout=l2)
# while True:
#     e, v = win.read()
#     print(e, v)
#     if e == None:
#         win.close()
#         break


l = [1, 5, 9]
l.insert(1, 'dos')
print(l)
