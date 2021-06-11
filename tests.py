import PySimpleGUI as ps


def mi_funcion():
    print('FUNCIONA')

layout = [
    [
        ps.ButtonMenu(
            'config', ['Menu', ['uno', 'dos', 'tres']], key=mi_funcion
        )
    ]
]
win = ps.Window(layout=layout, font=('Helvetica 16'))
while True:
    e, _ = win.read()
    e()
    if e is None:
        win.close()
        break

'FUNCIONA CARAJO AAAAAAAAAAAA JAJAJAJAJA'
