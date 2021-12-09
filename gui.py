import PySimpleGUI as sg
import json
import gspread

from oauth2client.service_account import ServiceAccountCredentials
from unidecode import unidecode

import personal_server
import forms_server
import prof_server

SCOPE = ['https://spreadsheets.google.com/feeds',
     'https://www.googleapis.com/auth/drive']

API_KEY_FILE = "key.json"

with open('config.json') as f:
  config = json.load(f)

port = config['port']

sg.theme('Default')
sg.change_look_and_feel('DefaultNoMoreNagging')

variants = {'Personal feedback': personal_server,
            'Class feedback': forms_server,
            'Professor feedback': prof_server,
            }

def get_ws():
    # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html

    # Authenticate using the signed key
    credentials = ServiceAccountCredentials.from_json_keyfile_name(API_KEY_FILE, SCOPE)
    gc = gspread.authorize(credentials)

    sheet_list = []

    for i, sheet in enumerate(gc.openall()):
        sheet_list.append([sheet.title])

    return sheet_list

server_choices = [x for x in variants.keys()]
sheet_list = get_ws()

left_col = [[sg.Text("Current port: ")],
            [sg.Text("Google sheet: ")],
            [sg.Text("Program variant: ")],
            ]

right_col = [[sg.Input(port, key='-PORT-', size=(6, 1))],
             [sg.InputCombo(sheet_list, size=(20, 1), key='-SHEET-')],
             [sg.InputCombo(server_choices, size=(20, 1), key='-SERVER-')],
             ]

layout = [[sg.Text('Pepper education server launcher', font=('Helvetica', 16))],
          [sg.Text('This launches the server on this machine.', font=('Helvetica', 10))],
          [sg.Text('You should thereafter launch the Pepper client.', font=('Helvetica', 10))],
          [sg.Column(left_col, element_justification='l'), sg.Column(right_col, element_justification='l')],
          [sg.Text(size=(50, 1), key='-CHOSEN SERVER-')],
          [sg.Text(size=(50, 1), key='-MESSAGE-')],
          [sg.Button('Launch', bind_return_key=True), sg.Button('Exit')]]

window = sg.Window('Pepper edu program', layout)

launch_bool = False

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        try:
            p.terminate()
        except NameError:
            print('No process was running yet.')
        break
    if values['-SERVER-']:
        window['-CHOSEN SERVER-'].update(values['-SERVER-'])
    if event == 'Launch':
        if values['-SERVER-'] in variants and values['-SHEET-'] and values['-PORT-']:
            launch_bool = True
            break
        else:
            window['-MESSAGE-'].update("Set the parameters before launch.")
# Finish up by removing from the screen
window.close()


if launch_bool:
    try:
        print(f"Launched server with {values['-SHEET-']}. Terminate server with Ctrl+C.")
        variants[values['-SERVER-']].main(values['-SHEET-'][0], int(values['-PORT-']))
    except KeyboardInterrupt:
        print("\nServer terminated by keyboard interrupt.")



