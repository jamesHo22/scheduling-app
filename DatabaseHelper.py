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
SPREADSHEET_ID = '1axzYqYD_jPpk99Zj_h-qfTfunXbLtzXmBragOJqS8t8'
LOG_RANGE = 'TimeLog!A2:E'
RECENT_ACTIVITIES_RANGE = 'RecentActivities!A3:A'
RECENT_COUNTS_RANGE = 'RecentActivities!B3:B'
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
                'dontPush/client_secret.json', SCOPES)
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
        spreadsheetId=SPREADSHEET_ID
    , range=LOG_RANGE,
        valueInputOption=VALUE_INPUT_OPTION, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

def getRecentActivities(service):
    '''
    service: a service object that is used to connect with google sheets
    returns: List of strings that are ordered by number of times entered
    '''
    # Get the information
    sheet = service.spreadsheets()
    resultAct = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RECENT_ACTIVITIES_RANGE).execute()
    activities = resultAct.get('values', [])
    lengthAct = len(activities)
    resultCounts = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RECENT_COUNTS_RANGE+str(2+lengthAct)).execute()
    counts = resultCounts.get('values', [])

    actCountList = []

    if not activities or not counts:
        print('No data found.')
    else:
        # reformat the data and sort
        i = 0
        while i < lengthAct:
            actCountList.append([activities[i][0], int(counts[i][0])])
            i += 1
        # Sort based on number of times done
        actCountList.sort(key=lambda x: x[1], reverse=True)
    
    return actCountList
        

if __name__ == '__main__':
    sheetsAuth()