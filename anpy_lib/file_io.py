import json
from openpyxl import Workbook
from anpy.utils import get_most_recent_monday

TEMP_SHEET_NAME = 'temp_sheet_anpy'
JSON_FILE_NAME = 'data.json'

TIMER_RUNNING = 0
TIMER_STOPPED = 1


def load_workbook(path):
    try:
        wb = load_workbook(path)
    except FileNotFoundError:
        wb = Workbook()
        wb.active.title = TEMP_SHEET_NAME
    return wb, path


def get_relevant_worksheet(workbook, date=None):
    reference_date = str(get_most_recent_monday(date))
    if reference_date not in workbook.sheetnames:
        workbook.create_sheet(title=reference_date)
    return workbook[reference_date]



def save_file(wb, path):
    wb.save(path)


def load_json(path):
    with open(path) as f:
        return json.load(f)
