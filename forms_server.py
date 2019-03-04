from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import socket
import subprocess

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# This needs to be your API key file
# NOTE: Currently I have a different key file, so I keep it commented
# API_KEY_FILE = "Macerata-b7cd0349db2e.json"
# API_KEY_FILE = "macerata-1549040199941-9b1795f038ec.json"
API_KEY_FILE = "key.json"


# The requested spreadsheet
SPREADSHEET = "Lez 1 02 26 Obiettivi (Responses)"


p = subprocess.Popen(["scp", "my_file.txt", "username@server:path"])
sts = os.waitpid(p.pid, 0)


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
                print(data.head(10))

        # TODO: Have code connect to a given form requested maybe by Pepper
        # TODO: Do calculations on received data


if __name__ == '__main__':
        host = socket.gethostname()  # get local machine name
        port = 8080  # Make sure it's within the > 1024 $$ <65535 range

        s = socket.socket()
        s.bind((host, port))

        s.listen(1)
        c, addr = s.accept()
        print("Connection from: " + str(addr))
        while True:
                data = c.recv(1024).decode('utf-8')
                if not data:
                        break
                print('From online user: ' + data)
                data = data.upper()
                c.send(data.encode('utf-8'))
                get_forms_data()

        c.close()
