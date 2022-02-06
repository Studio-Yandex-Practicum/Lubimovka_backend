from datetime import datetime as dt

from google.oauth2 import service_account
from googleapiclient.discovery import build

from config.settings.base import (
    GOOGLE_EXPORT_KEYS,
    GOOGLE_RANGE,
    GOOGLE_SCOPES,
    GOOGLE_SHEET_ID,
    PARTICIPATION_FILE_PATH,
)

KEYS = GOOGLE_EXPORT_KEYS
PATH = PARTICIPATION_FILE_PATH
RANGE = GOOGLE_RANGE
SCOPES = GOOGLE_SCOPES
SHEET_ID = GOOGLE_SHEET_ID


def build_service():
    scopes = [SCOPES]
    # try:
    credentials = service_account.Credentials.from_service_account_info(KEYS)
    # except ValueError:
    # return
    scoped_credentials = credentials.with_scopes(scopes)
    return build("sheets", "v4", credentials=scoped_credentials)


def get_instance_values(instance) -> dict:
    instance_created = str(dt.now().date())
    instance_file_path = PATH + str(instance.file.url)
    instance_number = " "
    return {
        "values": [
            [
                instance_number,
                instance_created,
                instance.first_name,
                instance.last_name,
                instance.birth_year,
                instance.city,
                str(instance.phone_number),
                instance.email,
                instance.festival_year,
                instance.year,
                instance.title,
                instance_file_path,
            ]
        ]
    }


def export_new_object(instance) -> None:
    value_input_option = "USER_ENTERED"
    body = get_instance_values(instance)
    service = build_service()
    request = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SHEET_ID,
            range=RANGE,
            valueInputOption=value_input_option,
            body=body,
        )
    )
    request.execute()
