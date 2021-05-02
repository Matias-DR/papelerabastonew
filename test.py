import PySimpleGUI as ps


col = ps.Col([[ps.Check('check')]])
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
