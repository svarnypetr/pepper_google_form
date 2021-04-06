import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import socket
import sys
import os
import re
from unidecode import unidecode

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

API_KEY_FILE = "key.json"
SPREADSHEET = "Lez04 (Responses)"
PORT = 6556  # Make sure it's within the > 1024 $$ <65535 range

# TODO for GUI:
# Need to collect SPREADSHEET
# Set the PORT
# Give clear instructions what to do with the program
# Make decision between the various approaches, e.g. prof, vs forms, ...
# Add clear instructions what to run from the other tools

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

#!!!Added here worksheet with Prof feedback
        worksheet = workbook.worksheet('Feedback').get_all_values()
        prof_df = pd.DataFrame(worksheet)
        prof_df.columns = prof_df.iloc[0]
        return prof_df


def remove_non_ascii(text):
    return unidecode(text)


def generate_output_sequence(prof, id):
        """
        Generates messages for the output based on the processed data.
        :param prof: {dataframe}
        :param id: {str} identifying the student
        :return: {string}
        """
        output_string = b''
        id_row = prof.loc[prof['matricola'] == id]

        # We get the student name
        output_string += remove_non_ascii(id_row.iloc[0]['nome']).encode("utf-8") + b' ' +\
                         remove_non_ascii(id_row.iloc[0]['cognome']).encode("utf-8") + b"%" +\
                         remove_non_ascii(id_row.iloc[0]['vote']).encode("utf-8") + b"%" +\
                         remove_non_ascii(id_row.iloc[0]['judgement']).encode("utf-8") + b"%"

        # for i in range(len(prof.columns)):
        #         # We add the vote and the judgement
        #         if prof.iloc[1, i]:
        #                 output_string += remove_non_ascii(id_row.iloc[0, i + 4]).encode("utf-8") + "%"      
        return output_string


if __name__ == '__main__':
        host = socket.gethostname()  # get local machine name
        port = PORT  # Make sure it's within the > 1024 $$ <65535 range
        test_run = False

        if "-t" in str(sys.argv):
                test_run = True

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        NUMBER_OF_FORMS = 100  # The number of connections the server accepts before shutting down
        run_count = 0

        matricola_pattern = r"^[0-9]{5}"

        prof_df = get_ws(SPREADSHEET)

        while run_count < NUMBER_OF_FORMS:
                s.listen(5)
                c, addr = s.accept()
                print("Connection from: " + str(addr))
                client_data = c.recv(2048).decode('utf-8')

                is_matched = re.findall(matricola_pattern, client_data)

                if is_matched:
                        output = generate_output_sequence(prof_df, client_data)

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
