import json
import datetime

TEMP_SHEET_NAME = 'temp_sheet_anpy'
JSON_FILE_NAME = 'data.json'

TIMER_RUNNING = 0
TIMER_STOPPED = 1



        

def load_workbook(path):
    try:
        wb = load_workbook(path)
    except FileNotFoundException:
        wb = Workbook()
        wb.active.title = TEMP_SHEET_NAME
    return wb, path

def save_file(wb, path):
    wb.save(path)

def load_json(path):
    with open(path) as f:
        return json.load(f)

def get_state
