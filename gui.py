import PySimpleGUI as sg

# TODO: based on https://pypi.org/project/PySimpleGUI/
# TODO: add also a dropdown for the available matricolas
# TODO: incorporate all the code and dropdown for the various approaches - prof etc.

# Define the window's contents
layout = [[sg.Text("What folder should be used?")],     # Part 2 - The Layout
          [sg.Input()],
          [sg.Button('Ok')]]

# Create the window
window = sg.Window('Pepper edu program', layout)      # Part 3 - Window Definition

# Display and interact with the Window
event, values = window.read()                   # Part 4 - Event loop or Window.read call

# Do something with the information gathered
print('Hello', values[0], "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()

