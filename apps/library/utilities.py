from datetime import datetime as dt

from google.oauth2 import service_account
from googleapiclient.discovery import build

from apps.info.models import Festival
from config.settings.base import GOOGLE_EXPORT_KEYS, GOOGLE_SHEET_ID, PARTICIPATION_FILE_PATH

KEYS = GOOGLE_EXPORT_KEYS
PATH = PARTICIPATION_FILE_PATH
SHEET_ID = GOOGLE_SHEET_ID


def generate_class_name_path(instance, filename):
    festival = Festival.objects.last()
    return f"{instance.__class__.__name__}/{festival.year}/{filename}"


def get_festival_year():
    if 7 <= dt.now().month <= 12:
        return dt.now().year + 1
    return dt.now().year


def export_new_object(obj):
    range = "Лист1"
    value_input_option = "USER_ENTERED"

    obj_created = str(dt.now().date())
    obj_file_path = PATH + str(obj.file.url)
    obj_number = "-укажите номер заявки-"
    value_range_body = {
        "values": [
            [
                obj_number,
                obj_created,
                obj.first_name,
                obj.last_name,
                obj.birth_year,
                obj.city,
                str(obj.phone_number),
                obj.email,
                obj.festival_year,
                obj.year,
                obj.title,
                obj_file_path,
            ]
        ]
    }

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    try:
        credentials = service_account.Credentials.from_service_account_info(KEYS)
    except ValueError:
        return
    scoped_credentials = credentials.with_scopes(scopes)
    service = build("sheets", "v4", credentials=scoped_credentials)

    request = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SHEET_ID,
            range=range,
            valueInputOption=value_input_option,
            body=value_range_body,
        )
    )
    request.execute()
