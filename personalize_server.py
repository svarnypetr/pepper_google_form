from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import socket
import subprocess
import os
from unidecode import unidecode

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

API_KEY_FILE = "key.json"
SPREADSHEET = "Lez11 (Responses)"
PORT = 6554  # Make sure it's within the > 1024 $$ <65535 range


def get_ws(sheet_name):
        # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
        # Load in the secret JSON key (must be a service account)
        # json_key = json.load(open(API_KEY_FILE))

        # Authenticate using the signed key
        credentials = ServiceAccountCredentials.from_json_keyfile_name(API_KEY_FILE, SCOPE)
        gc = gspread.authorize(credentials)

        print("The following sheets are available")
        for sheet in gc.openall():
                print("{} - {}".format(sheet.title, sheet.id))

        # Open up the workbook based on the spreadsheet name
        workbook = gc.open(sheet_name)

        # Get selected worksheet
        worksheet = workbook.worksheet('Form Responses 1').get_all_values()
        student_df = pd.DataFrame(worksheet)
        student_df.columns = student_df.iloc[0]
        student_df = student_df.drop(student_df.index[0])

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
        output_string = ''
        id_row = students.loc[students['matricola'] == id]

        # We get the student name
        output_string += str(id_row.iloc[0]['nome']) + ' ' + str(id_row.iloc[0]['cognome']) + "%"

        for i in range(len(general.columns) - 2):
                # We add the question
                if general.iloc[1, i]:
                        output_string += str(general.iloc[1, i]) + "%"
                # We add his answer
                output_string += remove_non_ascii(id_row.iloc[0, 2*i + 4]).encode("utf-8") + "%"
                # We add his result
                if id_row.iloc[0, 2*i + 5] == 1:
                        output_string += str(id_row.iloc[0, 2*i + 5]) + "%"
                else:
                        output_string += str(general.iloc[2, i]) + "%"
        return output_string


if __name__ == '__main__':
        host = socket.gethostname()  # get local machine name
        port = PORT  # Make sure it's within the > 1024 $$ <65535 range

        s = socket.socket()
        s.bind((host, port))
        NUMBER_OF_FORMS = 5  # TODO: This is the number of connections the server accepts before shutting down
        run_count = 0
        while run_count < NUMBER_OF_FORMS:
                s.listen(1)
                c, addr = s.accept()
                print("Connection from: " + str(addr))
                client_data = c.recv(1024).decode('utf-8')

                while client_data == '81513':
                        if client_data == 'stop':
                                break

                        students_df, general_df = get_ws(SPREADSHEET)

                        output = generate_output_sequence(students_df, general_df, client_data)

                        c.send(output.encode('utf-8'))
                        client_data = ''
                        c.close()
                run_count += 1
                if client_data == 'stop':
                        break
