import PySimpleGUI as ps


# rcs_col = ps.Col([[ps.Check('check')]], key='col')
col = ps.Col([[ps.Check('check')]], key='col', scrollable=True, size=(400, 350))
col.AddRow(ps.In('nada'), ps.B('ok'))
layout = [
    [
        col
    ]
]
win = ps.Window('test', layout=layout)
while True:
    e, _ = win.read()
    if e == None:
        win.close()
        break
    if e == 'ok':
        it = iter([1, 2, 3])
        print(*it)
        win.extend_layout(win['col'], [[ps.In('asd')]])
