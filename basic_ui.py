#!/usr/bin/env python3

from anpy_lib import file_io
from anpy_lib import column_creation
from anpy_lib import time_manage
import datetime as dt

PATH = 'basic_log.xlsx'
JSON_PATH = 'data.json'

_temp_subjects = 'temp1 temp2 temp3 temp4'.split(' ')

wb = file_io.load_workbook(PATH)
worksheet_ready, ws = file_io.get_relevant_worksheet(wb)
try:
    m = time_manage.Manager.from_json(file_io.load_json(JSON_PATH))
except FileNotFoundError:
    m = time_manage.Manager(dt.time(10, 0),
                            dt.date.today(),
                            _temp_subjects,
                            [c.__name__
                             for c
                             in column_creation.DEFAULT_COLUMNS])

if not worksheet_ready:
    column_creation.create_stat_columns()
    column_creation.create_subjects(_temp_subjects)
    column_creation.Column.make_all(ws)


def select_from_menu(items):
    for idx, item in enumerate(items):
        print(idx, item)
    try:
        result = int(input("Please choose a number.\n> "))
    except ValueError:
        print('Invalid')
    while result < 0 or result >= len(items):
        try:
            result = int(input("Please choose a number.\n> "))
        except ValueError:
            pass
        print('Invalid')
    return result


while True:
    if m.timer_running:
        print("Timer for {} is running".format(m.cur_subject))
        choice = select_from_menu(('stop', 'finish', 'cancel', 'quit'))
        if choice == 0:
            m.stop_timer()
            m.export_to_json(JSON_PATH)
        if choice == 1:
            m.stop_timer()
            m.export_to_json(JSON_PATH)
            m.write_data(ws, dt.time(10, 30))
            break
        if choice == 3:
            quit()
    else:
        choice = select_from_menu(m.subjects)
        m.start_timer(choice)
        m.export_to_json(JSON_PATH)


file_io.save_file(wb, PATH)
