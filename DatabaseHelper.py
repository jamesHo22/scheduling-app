# This helper class contains all the methods 
# required to access various data sources
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1axzYqYD_jPpk99Zj_h-qfTfunXbLtzXmBragOJqS8t8'
SAMPLE_RANGE_NAME = 'TimeLog!A2:E'
VALUE_INPUT_OPTION = 'USER_ENTERED'

def getSheetsService():
    """
    Asks user for google account information to access their google sheets. 

    Returns: a resource for interacting with API
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'dontPush/client_secret_738943635369-srdeg74vajc0qo1jcq5hudfmepb024iq.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    
    service = build('sheets', 'v4', credentials=creds)
    return service

def addLogEntry(service, logMessage):
    # Call the Sheets API
    values = [[str(datetime.datetime.now()), logMessage]]
    body = {
        'values': values
    }
    
    result = service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
        valueInputOption=VALUE_INPUT_OPTION, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

    # sheet = service.spreadsheets()
    # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    #                             range=SAMPLE_RANGE_NAME).execute()
    # values = result.get('values', [])

    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, Major:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s' % (row[0], row[4]))


if __name__ == '__main__':
    sheetsAuth()