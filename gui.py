import PySimpleGUI as sg

# TODO: add also a dropdown for the available matricolas
# TODO: incorporate all the code and dropdown for the various approaches - prof etc.
# TODO for GUI:
# Need to collect SPREADSHEET
# Set the PORT
# Give clear instructions what to do with the program
# Make decision between the various approaches, e.g. prof, vs forms, ...
# Add clear instructions what to run from the other tools

variants = {'Personal feedback': 'personal_server.py',
            'Class feedback': 'forms_server.py',
            'Professor feedback': 'prof_server.py',
            }

server_choices = [x for x in variants.keys()]

layout = [[sg.Text("What folder should be used?")],
          [sg.Input(key='-FOLDER-', enable_events=True)],
          [sg.Text("What matricola folder should be used?")],
          [sg.Input(key='-MATRICOLA-', enable_events=True)],
          [sg.Text("What variant of the program you want to run?")],
          [sg.InputCombo(server_choices, size=(20, 1), key='-SERVER-')],
          #          [sg.Listbox(server_choices, size=(30, len(server_choices)), key='-SERVER-')],
          [sg.Text(size=(25, 1), key='-CHOSEN SERVER-')],
          [sg.Text(size=(25, 1), key='-MESSAGE-')],
          [sg.Button('Launch'), sg.Button('Exit')]]


window = sg.Window('Pepper edu program', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if values['-SERVER-']:
        window['-CHOSEN SERVER-'].update(values['-SERVER-'])
    if event == 'Launch':
        launch_str = f"We launch the app with {values['-FOLDER-']}."
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

