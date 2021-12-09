import gspread
import json
import os
import pandas as pd
import socket
import sys

from oauth2client.service_account import ServiceAccountCredentials
from unidecode import unidecode


SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# This needs to be your API key file
API_KEY_FILE = "key.json"


# The requested spreadsheet
SPREADSHEET = "Lez04 (Responses)"
PORT = 6553  # Make sure it's within the > 1024 $$ <65535 range


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
        sheet_data = pd.DataFrame(sheet.get_all_records())

        return sheet_data


def get_ws(sheet_name, test_run):
        # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
        # Load in the secret JSON key (must be a service account)
        # json_key = json.load(open(API_KEY_FILE))

        # Authenticate using the signed key
        credentials = ServiceAccountCredentials.from_json_keyfile_name(API_KEY_FILE, SCOPE)
        gc = gspread.authorize(credentials)

        if test_run:
                sheet_name = SPREADSHEET

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
        output_string = b''

        first_row_length = len(ws[0])
        for i in range(first_row_length - 2):
                # We read the question and add the question, if any. We keep % as separator.
                if ws[1][i]:
                        output_string += remove_non_ascii(ws[1][i]).encode("utf-8") + b"%"
                # We read the answer and add it, if any. We keep % as separator
                if ws[2][i]:
                        output_string += remove_non_ascii(ws[2][i]).encode("utf-8") + b"%"
                # each cell we turn the numbers into percent without decimal value, % will be then our separator
                output_string += "{:.0%}".format(float(ws[0][i])).encode("utf-8")
        output_string += "{:.0%}".format(float(ws[0][-2])).encode("utf-8") + "{:.0%}".format(float(ws[0][-1])).encode("utf-8")
        return output_string


def main(sheet, port):
        host = socket.gethostname()  # get local machine name
        test_run = False

        if "-t" in str(sys.argv):
                test_run = True

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        NUMBER_OF_FORMS = 6  # The number of connections the server accepts before shutting down
        run_count = 0
        ws = get_ws(sheet, test_run)
        while run_count < NUMBER_OF_FORMS:

                s.listen(5)
                c, addr = s.accept()
                print("Connection from: " + str(addr))
                while True:
                        data = c.recv(1024).decode('utf-8')
                        if data == 'stop':
                                break
                        output = generate_output_sequence(ws)
                        c.send(output)
                        if output:
                                break

                c.close()
                run_count += 1
                if data == 'stop':
                        c.close()
                        break


if __name__ == '__main__':
        main(SPREADSHEET, PORT)
