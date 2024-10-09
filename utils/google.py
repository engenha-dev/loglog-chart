import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from utils.ids import get_ids

SCOPES_SHEETS = ["https://www.googleapis.com/auth/spreadsheets"]
SCOPES_DRIVE = ["https://www.googleapis.com/auth/drive"]


def authenticate_api(scope, token_file, credentials_file):
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scope)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scope)
            creds = flow.run_local_server(port=0)

        with open(token_file, "w", encoding="UTF-8") as token:
            token.write(creds.to_json())

    return creds


def get_service(api_name, api_version, scopes, token_file, credentials_file):
    creds = authenticate_api(scopes, token_file, credentials_file)
    return build(api_name, api_version, credentials=creds)


def get_sheet_service():
    return get_service(
        "sheets",
        "v4",
        SCOPES_SHEETS,
        "auth/token_sheets.json",
        "auth/client_secrets.json",
    ).spreadsheets()


def get_drive_service():
    return get_service(
        "drive", "v3", SCOPES_DRIVE, "auth/token_drive.json", "auth/client_secrets.json"
    )


def get_title(sheet, spreadsheet_id):
    SAMPLE_RANGE_NAME = "Impressao!P22"
    result = (
        sheet.values()
        .get(spreadsheetId=spreadsheet_id, range=SAMPLE_RANGE_NAME)
        .execute()
    )

    if title_value := result.get("values", []):
        return title_value[0][0]

    return "COORDENOGRAMA"


def upload_drive(img_buffer, file_name):
    FOLDER_ID = get_ids("drive")
    drive_service = get_drive_service()

    file_metadata = {"name": file_name, "parents": [FOLDER_ID]}
    media = MediaIoBaseUpload(img_buffer, mimetype="image/jpeg")
    drive_service.files().create(body=file_metadata, media_body=media).execute()
