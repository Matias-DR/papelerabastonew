import os
import asyncio
from PySimpleGUI import(
    Window, Button
)
from multiprocessing import Process
from time import sleep

def init():
	os.system('git config user.name \'papelerabasto\'')
	os.system('git config user.email \'papelera.abasto@gmail.com\'')
	os.system('git remote add pa <link>')
	os.system('git add .')
	os.system('git commit -m \'init-auto-commit\'')
	os.system('git branch -m bu')
	os.system('git push pa bu')
	os.system('git branch -m main')

def event():
	os.system('git add .')
	os.system('git commit -m \'auto-commit\'')
	os.system('git push pa main')

async def bu():
    while True:
        # sleep(1800)
        os.system('git add .')
        os.system('git commit -m \'async-auto-commit\'')
        os.system('git branch -m bu')
        os.system('git push pa bu')
        os.system('git branch -m main')

def main():
    Process.start(asyncio.run(bu()))
    print('llega')
    layout = [
        [
            Button('Click for generate event')
        ]
    ]
    win = Window(layout=layout)
    while True:
        if win.read()[0] == None:
            win.close()
            break
        else:
            event()

if __name__ == "__main__":
    main()
