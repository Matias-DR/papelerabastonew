import PySimpleGUI as ps
import constant as ct


# ACÁ SE ENCUENTRA LA MANERA DE CAMBIAR LA FUENTE Y HACER A LOS BOTONES DECENTES
ps.theme('PapelerAbasto')
lt = [
    [
        ps.Input(default_text='', size=(4, 4)),
        ps.Button(button_text='', image_data=ct.PNG_DELETE, image_size=(25, 25), border_width=0,
                  button_color=('#232323', '#232323'))
    ]
]
win = ps.Window(title='aa', layout=lt, font=('Arial 18'))
while True:
    e, _ = win.read()
    if e is None:
        win.close()
        break
