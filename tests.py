import PySimpleGUI as ps


layout = [
    [
        ps.ButtonMenu(
            'config', ['Menu', ['uno', 'dos', 'tres']], key='bm'
        )
    ]
]
win = ps.Window(layout=layout, font=('Helvetica 16'))
while True:
    e, v = win.read()
    print(e, v)
    if e is None:
        win.close()
        break
