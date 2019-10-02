from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
# import matplotlib.pyplot as plt
import json
import socket
import subprocess
import os

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# This needs to be your API key file
# NOTE: Currently I have a different key file, so I keep it commented
# API_KEY_FILE = "Macerata-b7cd0349db2e.json"
# API_KEY_FILE = "macerata-1549040199941-9b1795f038ec.json"
API_KEY_FILE = "key.json"


# The requested spreadsheet
SPREADSHEET = "11 lesson (Responses)"


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
        column_names_original = list(data)  # TODO: test, maybe superfluous
        column_names = {}  # TODO: test, maybe superfluous
        for name in column_names_original:  # TODO: test, maybe superfluous
            column_names[name] = name.lower().replace(' ', '')    # TODO: test, maybe superfluous

        data.rename(columns=column_names, inplace=True)  # TODO: test, maybe superfluous
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
        worksheet = workbook.worksheet('Calculations')

        return worksheet


# def make_data_viz(df):
#         """
#         Based on processed data generates a histogram that is then saved and scp-d to Pepper.
#         :param df: {pandas.DataFrame}
#         :return: None
#         """
#         fig, ax = plt.subplots()
#         image_name = 'image.png'
#         fig.savefig(image_name)
#         # pepper_img_location = "nao@10.10.60.137:/home/nao/.local/share/PackageManager/apps/connectgoogleforms-00573d/html/image.png"
#         # p = subprocess.Popen(['scp', image_name, pepper_img_location])
#         # sts = os.waitpid(p.pid, 0)
#         return None


def generate_output_sequence(ws):
        """
        Generates messages for the output based on the processed data.
        :param ws: {worksheet}
        :return: {string}
        """
        output_string = '';

        # loop through first row until you find an empty cell
        i = 1
        while not (ws.cell(1, i).value == ""):
                # each cell we turn the numbers into percent without decimal value, % will be then our separator
                output_string += "{:.0%}".format(float(ws.cell(1, i).value))
                i += 1
        return output_string


if __name__ == '__main__':
        host = socket.gethostname()  # get local machine name
        port = 6555  # Make sure it's within the > 1024 $$ <65535 range

        s = socket.socket()
        s.bind((host, port))
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

                        # df = get_forms_data()
                        ws = get_ws(SPREADSHEET)

                        output = generate_output_sequence(ws)
                        # make_data_viz(df)

                        c.send(output.encode('utf-8'))

                c.close()
                run_count += 1
