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

# This needs to be your API key file
# NOTE: Currently I have a different key file, so I keep it commented
# API_KEY_FILE = "Macerata-b7cd0349db2e.json"
# API_KEY_FILE = "macerata-1549040199941-9b1795f038ec.json"
API_KEY_FILE = "key.json"


# The requested spreadsheet
SPREADSHEET = "pepper competenza 2 (Responses)"


def get_forms_data():
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
        workbook = gc.open(SPREADSHEET)

        # Get the first sheet
        sheet = workbook.worksheet('Calculations')

        # Extract all data into a dataframe
        data = pd.DataFrame(sheet.get_all_records())

        # Do some minor cleanups on the data
        # Rename the columns to make it easier to manipulate
        # The data comes in through a dictionary so we can not assume order stays the
        # same so must name each column
        # Currently columns are renamed without knowing their names in order to work with any form
        # data.timestamp = pd.to_datetime(data.timestamp)

        # NOTE: This code will allow us to access/work with data from the last 2 minutes
        # pd.Timestamp.now()
        # pd.date_range(pd.Timestamp.now(), periods=2, freq='1min')[1]

        # Prints the first 10 lines of results

        return data


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

        # Get the first sheet
        worksheet = workbook.worksheet('Calculations').get_all_values()

        return worksheet


def remove_non_ascii(text):
    return unidecode(text)


def generate_output_sequence(ws):
        """
        Generates messages for the output based on the processed data.
        :param ws: {worksheet}
        :return: {string}
        """
        output_string = ''

        first_row_length = len(ws[0])
        for i in range(first_row_length - 2):
                # We read the question and add the question, if any. We keep % as separator.
                if ws[1][i]:
                        output_string += remove_non_ascii(ws[1][i]).encode("utf-8") + "%"
                # We read the answer and add it, if any. We keep % as separator.
                if ws[2][i]:
                        output_string += remove_non_ascii(ws[2][i]).encode("utf-8") + "%"
                # each cell we turn the numbers into percent without decimal value, % will be then our separator
                output_string += "{:.0%}".format(float(ws[0][i]))
        output_string += "{:.0%}".format(float(ws[0][-2])) + "{:.0%}".format(float(ws[0][-1]))
        return output_string


if __name__ == '__main__':
        host = socket.gethostname()  # get local machine name
        port = 6554  # Make sure it's within the > 1024 $$ <65535 range

        s = socket.socket()
        s.bind(('', port))
        NUMBER_OF_FORMS = 5  # TODO: This is the number of connections the server accepts before shutting down
        run_count = 0
        while run_count < NUMBER_OF_FORMS:
                s.listen(1)
                c, addr = s.accept()
                print("Connection from: " + str(addr))
                while True:
                        data = c.recv(1024).decode('utf-8')
                        if data == 'stop':
                                break

                        ws = get_ws(SPREADSHEET)

                        output = generate_output_sequence(ws)

                        c.send(output.encode('utf-8'))

                c.close()
                run_count += 1
                if data == 'stop':
                        break
