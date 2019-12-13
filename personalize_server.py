from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import socket
import subprocess
import os

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

API_KEY_FILE = "key.json"
SPREADSHEET = "Lez11 (Responses)"
PORT = 6554  # Make sure it's within the > 1024 $$ <65535 range


def get_ws(sheet_name, worksheet_name):
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
        worksheet = workbook.worksheet(worksheet_name).get_all_values()
        ws_df = pd.DataFrame(worksheet)
        ws_df.columns = ws_df.iloc[0]
        ws_df = ws_df.drop(ws_df.index[0])

        return ws_df


def generate_output_sequence(ws, id):
        """
        Generates messages for the output based on the processed data.
        :param ws: {worksheet}
        :return: {string}
        """
        output_string = ''
        id_row = ws.loc[ws['matricola'] == id]

        # first_row_length = len(ws[0])
        # for i in range(first_row_length - 2):
        #         # We read the question and add the question, if any. We keep % as separator.
        #         if ws[1][i]:
        #                 output_string += ws[1][i] + "%"
        #         # We read the answer and add it, if any. We keep % as separator.
        #         if ws[2][i]:
        #                 output_string += ws[2][i] + "%"
        #         # each cell we turn the numbers into percent without decimal value, % will be then our separator
        # #         output_string += "{:.0%}".format(float(ws[0][i]))
        # # output_string += ws[0][-2] + ws[0][-1]
        output_string = str(id_row)
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
                while True:
                        client_data = c.recv(1024).decode('utf-8')
                        if client_data == 'stop':
                                break

                        ws_df = get_ws(SPREADSHEET, 'Form Responses 1')
                        # ws_calculations_df = get_ws(SPREADSHEET, 'Calculations')

                        output = generate_output_sequence(ws_df, client_data)

                        c.send(output.encode('utf-8'))

                c.close()
                run_count += 1
                if client_data == 'stop':
                        break
