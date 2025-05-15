import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import json
import streamlit as st


SHEET_ID = "1_QKBHGAeazIOg1oXDl05NQCJM-W0JJ_n4k7jHtvRg04"
SHEET_NAME = "Battery Serial Code Scanning Record"


def connect_to_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    service_account_info = json.loads(st.secrets["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    return sheet


def get_latest_pack_serial(capacity_code="14"):
    sheet = connect_to_sheet()
    rows = sheet.get_all_values()
    now = datetime.datetime.now()
    year = str(now.year)[-2:]
    month_letter = "ABCDEFGHIJKL"[now.month - 1]
    prefix = f"{year}{month_letter}{capacity_code}"

    sequence = 0
    for row in rows[1:]:
        if len(row) >= 1 and str(row[0]).startswith(prefix):
            sequence += 1
    return f"{prefix}{sequence + 1:03d}"


def save_record_to_sheet(record):
    sheet = connect_to_sheet()
    row = [
        str(record.get("PackSerial", "")),
        str(record.get("BMSSerial", "")),
        str(record.get("Timestamp", ""))
    ]
    sheet.append_row(row)