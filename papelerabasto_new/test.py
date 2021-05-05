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

l = ['as'] + ['otro_valor']

l += ['1', '3', '4']

print(l)
