import PySimpleGUI as sg
import json
import gspread

from oauth2client.service_account import ServiceAccountCredentials
from unidecode import unidecode

SCOPE = ['https://spreadsheets.google.com/feeds',
     'https://www.googleapis.com/auth/drive']

API_KEY_FILE = "key.json"

with open('config.json') as f:
  config = json.load(f)

port = config['port']

sg.theme('Default')
sg.change_look_and_feel('DefaultNoMoreNagging')

variants = {'Personal feedback': 'personal_server.py',
            'Class feedback': 'forms_server.py',
            'Professor feedback': 'prof_server.py',
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

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if values['-SERVER-']:
        window['-CHOSEN SERVER-'].update(values['-SERVER-'])
    if event == 'Launch':
        launch_str = f"We launch the app with {values['-SHEET-']}."
        window['-MESSAGE-'].update(launch_str)


# Finish up by removing from the screen
window.close()

# Popup for errors
# text_input = values[0]
# sg.popup('You entered', text_input)

# List of options -> fixed list of options for prof/etc. but collected from Google for the matricolas
# choices = ('Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple', 'Chartreuse')
# [sg.Listbox(choices, size=(15, len(choices)), key='-COLOR-')],

# Debug prints in separate debug window
# sg.Print('Re-routing the stdout', do_not_reroute_stdout=False)
# print('This is a normal print that has been re-routed.')
# https://pysimplegui.readthedocs.io/en/latest/cookbook/#recipe-printing not reroute possibly

# Subprocess launch
# CHROME = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
#
#     if event == 'Chrome':
#
#         sg.execute_command_subprocess(CHROME)

