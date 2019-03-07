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
SPREADSHEET = "Lez 1 02 26 Obiettivi (Responses)"


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
        sheet = workbook.sheet1

        # Extract all data into a dataframe
        data = pd.DataFrame(sheet.get_all_records())

        # Do some minor cleanups on the data
        # Rename the columns to make it easier to manipulate
        # The data comes in through a dictionary so we can not assume order stays the
        # same so must name each column
        # Currently columns are renamed without knowing their names in order to work with any form
        column_names_original = list(data)
        column_names = {}
        for name in column_names_original:
            column_names[name] = name.lower().replace(' ', '')

        data.rename(columns=column_names, inplace=True)
        data.timestamp = pd.to_datetime(data.timestamp)

        # NOTE: This code will allow us to access/work with data from the last 2 minutes
        # pd.Timestamp.now()
        # pd.date_range(pd.Timestamp.now(), periods=2, freq='1min')[1]

        # Prints the first 10 lines of results

        return data


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


def generate_output_message(df):
        """
        Generates messages for the output based on the processed data.
        :param df: {pandas.DataFrame}
        :return: {string}
        """
        counted = df.iloc[:, 2].value_counts()
        total = counted.sum(axis=0)
        percentage_correct = float(counted.ix['Si']) / total
        if percentage_correct > 0.6:
                output_string = 'Yes'
        else:
                output_string = 'No'
        return output_string


if __name__ == '__main__':
        host = socket.gethostname()  # get local machine name
        port = 8079  # Make sure it's within the > 1024 $$ <65535 range

        s = socket.socket()
        s.bind((host, port))
        NUMBER_OF_FORMS = 5
        run_count = 0
        while run_count < NUMBER_OF_FORMS:
                s.listen(1)
                c, addr = s.accept()
                print("Connection from: " + str(addr))
                while True:
                        data = c.recv(1024).decode('utf-8')
                        if data == 'stop':
                                break

                        df = get_forms_data()

                        output = generate_output_message(df)
                        # make_data_viz(df)

                        c.send(output.encode('utf-8'))

                c.close()
                run_count += 1
