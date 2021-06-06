import PySimpleGUI as ps

def render_layout():
    return [
        [
            ps.Button('event'),
            ps.Input('', key='una llave')
        ]
    ]

win = ps.Window(layout=render_layout())

while True:
    e, v = win.read()
    if e is None:
        win.close()
        break
    print(e, v)
    print('print de los valores: ', win.ReturnValuesDictionary)
    print(bool(int(v['una llave'])))
