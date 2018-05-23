
TEMP_SHEET_NAME = 'temp_sheet_anpy'

def load_file(path):
    try:
        wb = load_workbook(path)
    except FileNotFoundException:
        wb = Workbook()
        wb.active.title = TEMP_SHEET_NAME
    return wb, path

def save_file(wb, path):
    wb.save(path)

