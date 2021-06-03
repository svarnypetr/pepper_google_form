import PySimpleGUI as sg

# TODO: add also a dropdown for the available matricolas
# TODO: incorporate all the code and dropdown for the various approaches - prof etc.
# TODO for GUI:
# Need to collect SPREADSHEET
# Set the PORT
# Give clear instructions what to do with the program
# Make decision between the various approaches, e.g. prof, vs forms, ...
# Add clear instructions what to run from the other tools

layout = [[sg.Text("What folder should be used?")],
          [sg.Input()],
          [sg.Text("What matricola folder should be used?")],
          [sg.Input()],
          [sg.Button('Ok'), sg.Button('Exit')]]


window = sg.Window('Pepper edu program', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

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

