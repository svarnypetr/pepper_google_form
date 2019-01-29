from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
SECRETS_FILE = "southern-range-230110-e86cb31f6665.json"
SPREADSHEET = "Hagen test form (sheet)"
# Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
# Load in the secret JSON key (must be a service account)
json_key = json.load(open(SECRETS_FILE))

# Authenticate using the signed key
credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, SCOPE)

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
        column_names = {'Time stamps': 'timestamp',
                        'Question 1': 'question',
                        }
        data.rename(columns=column_names, inplace=True)
        data.timestamp = pd.to_datetime(data.timestamp)
        import ipdb; ipdb.set_trace()

        # pd.Timestamp.now()
        # pd.date_range(pd.Timestamp.now(), periods=2, freq='1min')[1]

        print(data.head())
