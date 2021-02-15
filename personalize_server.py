import gspread
import json
import os
import pandas as pd
import re
import socket
import subprocess
import sys

from oauth2client.service_account import ServiceAccountCredentials
from unidecode import unidecode

SCOPE = ['https://spreadsheets.google.com/feeds',
     'https://www.googleapis.com/auth/drive']

API_KEY_FILE = "key.json"
SPREADSHEET = "Lez04 (Responses)"
PORT = 6555  # Make sure it's within the > 1024 $$ <65535 range


def get_ws(test_run):
    # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html

    # Authenticate using the signed key
    credentials = ServiceAccountCredentials.from_json_keyfile_name(API_KEY_FILE, SCOPE)
    gc = gspread.authorize(credentials)

    sheet_list = []

    chosen_sheet = False
    if test_run:
        chosen_sheet = True
        sheet_name = SPREADSHEET
    else:
        print("The following sheets are available")
        for i, sheet in enumerate(gc.openall()):
            sheet_list.append([sheet.title])
            # print("{}.: {} - {}".format(str(i + 1), sheet.title, sheet.id))
            print("{}. {}".format(str(i + 1), sheet.title))  # assumption the ID is not needed

    if sheet_list:
        while not chosen_sheet:
            chosen_sheet = int(input(f"Which sheet should be used? (input number 1-{len(sheet_list)}) "))
            if chosen_sheet in range(1, len(sheet_list)):
                sheet_name = sheet_list[chosen_sheet - 1][0]
            else:
                print(f"Sheet number needs to be in range 1-{len(sheet_list) + 1}")
                chosen_sheet = False
    if not sheet_list and not test_run:
        print("No sheets available.")
        return
    # Open up the workbook based on the spreadsheet name
    # sheet_name = "Lez04 (Responses)"  #WIP
    workbook = gc.open(sheet_name)

    # Get selected worksheet
    worksheet = workbook.worksheet('Form Responses 1').get_all_values()
    student_df = pd.DataFrame(worksheet)
    student_df.columns = student_df.iloc[0]

    worksheet = workbook.worksheet('Calculations').get_all_values()
    general_df = pd.DataFrame(worksheet)
    return student_df, general_df


def remove_non_ascii(text):
    return unidecode(text)

def generate_output_sequence(students, general, id):
    """
    Generates messages for the output based on the processed data.
    :param students: {dataframe}
    :param general: {dataframe}
    :param id: {str} identifying the student
    :return: {string}
    """
    output_string = b''
    id_row = students.loc[students['matricola'] == id]

    # We get the student name
    output_string += remove_non_ascii(id_row.iloc[0]['nome']).encode("utf-8") + b' ' + remove_non_ascii(id_row.iloc[0]['cognome']).encode("utf-8") + b"%"

    for i in range(len(general.columns) - 2):
        # We add the question
        if general.iloc[1, i]:
            output_string += remove_non_ascii(general.iloc[1, i]).encode("utf-8") + b"%"
        # We add his answer
        output_string += remove_non_ascii(id_row.iloc[0, i + 4]).encode("utf-8") + b"%"
        # We add correct result
        output_string += remove_non_ascii(general.iloc[2, i]).encode("utf-8") + b"%"
      
    return output_string


if __name__ == '__main__':
    host = socket.gethostname()  # get local machine name
    port = PORT  # Make sure it's within the > 1024 $$ <65535 range
    test_run = False

    try:
        ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip.connect(("8.8.8.8", 80))
        print('Server at:', ip.getsockname()[0])
    except:
        print("Failed to connect to the internet.")

    if "-t" in str(sys.argv):
        test_run = True

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    NUMBER_OF_FORMS = 100  # The number of connections the server accepts before shutting down
    run_count = 0

    matricola_pattern = r"^[0-9]{5}"

    students_df, general_df = get_ws(test_run)

    while run_count < NUMBER_OF_FORMS:
        s.listen(5)
        c, addr = s.accept()
        print("Connection from: " + str(addr))
        client_data = c.recv(2048).decode('utf-8')

        is_matched = re.findall(matricola_pattern, client_data)

        if is_matched:
            output = generate_output_sequence(students_df, general_df, client_data)

            c.send(output)
            client_data = ''
            c.close()
        run_count += 1

        if not is_matched and client_data != 'stop':
            output = "matricola_error"
            print(output, "attempted to send: {}".format(client_data))
            c.send(output.encode('utf-8'))
            c.close()

        if client_data == 'stop':
            c.close()
            break
