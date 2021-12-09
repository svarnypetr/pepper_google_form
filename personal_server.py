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
PORT = 6558  # Make sure it's within the > 1024 $$ <65535 range


def get_ws(sheet_name, test_run):
    # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html

    # Authenticate using the signed key
    credentials = ServiceAccountCredentials.from_json_keyfile_name(API_KEY_FILE, SCOPE)
    gc = gspread.authorize(credentials)

    if test_run:
        sheet_name = SPREADSHEET

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


def main(sheet, PORT):
    host = socket.gethostname()  # get local machine name
    port = PORT  # Make sure it's within the > 1024 $$ <65535 range
    test_run = False

    if "-t" in str(sys.argv):
        test_run = True

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(('', port))
    NUMBER_OF_FORMS = 100  # The number of connections the server accepts before shutting down
    run_count = 0

    matricola_pattern = r"^[0-9]{5}"

    students_df, general_df = get_ws(sheet, test_run)

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


if __name__ == '__main__':
    main(SPREADSHEET, PORT)
