from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
SECRETS_FILE = "Macerata-b7cd0349db2e.json"
SPREADSHEET = "Lez 1 02 26 Obiettivi (Responses)"
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

# import datetime, schedule, request
#
# TIME = [('17.04.2011', '06:41:44', 'abc.php?xxx'),
#     ('17.04.2011', '07:21:31', 'abc.php?yyy'),
#     ('17.04.2011', '07:33:04', 'abc.php?zzz'),
#     ('17.04.2011', '07:41:23', 'abc.php?www')]
#
# def job():
#     global TIME
#     date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
#     for i in TIME:
#         runTime = i[0] + " " + i[1]
#         if i and date == str(runTime):
#             request.get(str(i[2]))
#
# schedule.every(0.01).minutes.do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)