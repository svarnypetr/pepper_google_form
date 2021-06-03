import PySimpleGUI as sg

# TODO: add also a dropdown for the available matricolas
# TODO: incorporate all the code and dropdown for the various approaches - prof etc.

# Define the window's contents
layout = [[sg.Text("What folder should be used?")],     # Part 2 - The Layout
          [sg.Input()],
          [sg.Button('Ok'), sg.Button('Exit')]]

# Create the window
window = sg.Window('Pepper edu program', layout)      # Part 3 - Window Definition

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

