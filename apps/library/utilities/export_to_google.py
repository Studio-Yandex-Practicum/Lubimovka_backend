import logging
from datetime import datetime as dt
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from apps.main.models import SettingGoogleExport
from config.logging import LOGGING_CONFIG
from config.settings.local import GOOGLE_PRIVATE_KEY, GOOGLE_PRIVATE_KEY_ID

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
URL = "https://www.googleapis.com/robot/v1/metadata/x509/lubimovka%40swift-area-340613.iam.gserviceaccount.com"
KEYS = {
    "type": "service_account",
    "private_key": GOOGLE_PRIVATE_KEY,
    "private_key_id": GOOGLE_PRIVATE_KEY_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "project_id": "swift-area-340613",
    "client_email": "lubimovka@swift-area-340613.iam.gserviceaccount.com",
    "client_id": "118115305686832196913",
    "client_x509_cert_url": URL,
}


def get_instance_values(instance, domain) -> dict:
    instance_created = str(dt.now().date())
    instance_file_path = domain + str(instance.file.url)
    return {
        "values": [
            [
                instance_created,
                instance.first_name,
                instance.last_name,
                instance.birth_year,
                instance.city,
                str(instance.phone_number),
                instance.email,
                instance.year,
                instance.title,
                instance_file_path,
            ]
        ]
    }


def build_service():
    try:
        credentials = service_account.Credentials.from_service_account_info(KEYS)
    except ValueError as error:
        logger.error(error, exc_info=True)
        return
    scoped_credentials = credentials.with_scopes(SCOPES)
    return build("sheets", "v4", credentials=scoped_credentials)


def get_sheet_id_by_title(service, spreadsheetId: str, sheet: str) -> Optional[int]:
    request = service.spreadsheets().get(spreadsheetId=spreadsheetId)
    try:
        spreadsheet = request.execute()
        for _sheet in spreadsheet["sheets"]:
            if _sheet["properties"]["title"] == sheet:
                return _sheet["properties"]["sheetId"]
    except HttpError as error:
        logger.error(error, exc_info=True)
        return


def set_borders(service, spreadsheetId: str, sheet: str) -> None:
    sheet_id = get_sheet_id_by_title(service=service, spreadsheetId=spreadsheetId, sheet=sheet)
    body = {
        "includeSpreadsheetInResponse": False,
        "requests": [
            {  # borders settings
                "updateBorders": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 200,
                        "startColumnIndex": 0,
                        "endColumnIndex": 10,
                    },
                    "bottom": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}},
                    "innerHorizontal": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1},
                    },
                    "innerVertical": {
                        "style": "SOLID",
                        "width": 1,
                        "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1},
                    },
                    "right": {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}},
                },
            },
            {  # header cells settings
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1},
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
                            "horizontalAlignment": "CENTER",
                            "textFormat": {
                                "foregroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0},
                                "fontSize": 10,
                                "bold": True,
                            },
                        },
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
                },
            },
            {  # freeze header cells
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheet_id,
                        "gridProperties": {"frozenRowCount": 1},
                    },
                    "fields": "gridProperties.frozenRowCount",
                },
            },
        ],
    }
    request = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheetId,
        body=body,
    )
    try:
        request.execute()
    except HttpError as error:
        logger.error(error, exc_info=True)
        return


def set_header(service, spreadsheetId: str, sheet: str) -> None:
    RANGE = sheet + "!A1"  # header starts at position "SheetTitle!A1"
    body = {
        "data": [
            {
                "range": RANGE,
                "values": [
                    [
                        "Дата создания заявки",
                        "Имя",
                        "Фамилия",
                        "Год рождения",
                        "Город",
                        "Телефон",
                        "Электронная почта",
                        "Год написания",
                        "Название",
                        "Ссылка на файл",
                    ]
                ],
            }
        ],
        "valueInputOption": "USER_ENTERED",
    }
    request = (
        service.spreadsheets()
        .values()
        .batchUpdate(
            spreadsheetId=spreadsheetId,
            body=body,
        )
    )
    try:
        request.execute()
    except HttpError as error:
        logger.error(error, exc_info=True)
        return


def export_new_object(instance, service, spreadsheetId: str, sheet: str, domain) -> Optional[bool]:
    RANGE = sheet
    value_input_option = "USER_ENTERED"
    body = get_instance_values(instance, domain)
    request = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheetId,
            range=RANGE,
            valueInputOption=value_input_option,
            body=body,
        )
    )
    try:
        request.execute()
    except HttpError as error:
        logger.error(error, exc_info=True)
        return
    service.spreadsheets().close()
    return True


def check_header_exists(service, spreadsheetId: str, sheet: str) -> bool:
    RANGE = sheet + "!A1"  # check position "SheetTitle!A1"
    request = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=RANGE)
    try:
        response = request.execute()
    except HttpError as error:
        logger.error(error, exc_info=True)
        return
    return response.get("values") is not None


def export(instance, domain) -> Optional[bool]:
    logger.info("Start export")
    SPREADSHEET_ID = SettingGoogleExport.get_setting("SPREADSHEET_ID")
    SHEET = SettingGoogleExport.get_setting("SHEET")
    RANGE = SHEET + "!A1"

    service = build_service()
    if service is None:
        return

    header_exists = check_header_exists(service=service, spreadsheetId=SPREADSHEET_ID, sheet=SHEET)
    if not header_exists:
        set_borders(service=service, spreadsheetId=SPREADSHEET_ID, sheet=SHEET)
        set_header(service=service, spreadsheetId=SPREADSHEET_ID, sheet=SHEET)
    return export_new_object(instance, service=service, spreadsheetId=SPREADSHEET_ID, sheet=RANGE, domain=domain)
