import sys
import os.path
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime
from time import time
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import FILES_AGENDA_MODULE_PATH
from general_functions import actually_date, export_json, read_json

path_credentials = FILES_AGENDA_MODULE_PATH / "credentials.json"
path_token = FILES_AGENDA_MODULE_PATH / "token.json"


def generate_service():
    creds = None

    if os.path.exists(path_token):
        creds = Credentials.from_authorized_user_file(path_token, ['https://www.googleapis.com/auth/calendar'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(path_credentials, ['https://www.googleapis.com/auth/calendar'])
            creds = flow.run_local_server(port=0)

        with open(path_token, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    return service

service = generate_service()

def create_event(content: str):
    content = content.split(",")
    summary = content[0].strip()
    start_datetime = content[1].strip()
    end_datetime = content[2].strip()
    unique_id = str(int(time()))

    event = {
            "id": unique_id,
            'summary': summary or "",
            'location': "",
            'description': "",
            'start': { 
                'dateTime': start_datetime or "",
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': end_datetime or "",
                'timeZone': 'America/Sao_Paulo',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 90}, 
                    {'method': 'popup', 'minutes': 30}   
                ]
            }
        }       
    
    event = service.events().insert(calendarId='primary', body=event).execute()

def delete_event(unique_id:str):
    service.events().delete(
        calendarId="primary",
        eventId=unique_id
    ).execute()

def events():
    now = datetime.now(ZoneInfo("America/Sao_Paulo")).astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=5, singleEvents=True,
                                          orderBy='startTime').execute()
    
    events = events_result.get('items', [])

    text = ""

    if not events:
        text += "Nenhum evento encontrado."

    else:
        text += "Próximos Eventos\n\n"

        for event in events:
            id = event['id'][:10]
            start = event['start'].get('dateTime', event['start'].get("date"))
            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M:%S")
            end = event['end'].get('dateTime', event['end'].get("date"))
            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M:%S")

            title = event['summary']

            text += f"Evento: {title}\n"
            text += f"Início: {start_dt}\n"
            text += f"Fim: {end_dt}\n"
            text += f"ID: {id}\n\n"
    
    return text

def format_response_ia(response:str):
    response = response.split(",")
    summary = response[0].strip()
    start_datetime = response[1].strip()
    start_dt = datetime.fromisoformat(start_datetime.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M:%S")
    end_datetime = response[2].strip()
    end_dt = datetime.fromisoformat(end_datetime.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M:%S")

    text = ""

    text += f"Evento: {summary}\n"
    text += f"Início: {start_dt}\n"
    text += f"Fim: {end_dt}\n"

    return text