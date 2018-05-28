#!/usr/bin/env python3

from anpy_lib import file_io
from anpy_lib import column_creation
from anpy_lib import time_manage
import datetime as dt
from anpy_lib.utils import get_most_recent_monday
import os

PATH = 'auto_log.xlsx'
JSON_PATH = 'auto.json'

subjects = 'sub0 sub1 sub2 sub3 sub4 sub5'.split(' ')

try:
    os.remove(PATH)
except FileNotFoundError:
    pass

try:
    os.remove(JSON_PATH)
except FileNotFoundError:
    pass

wb = file_io.load_workbook(PATH)
date = dt.date(2018, 5, 5)
worksheet_ready, ws = file_io.get_relevant_worksheet(wb, date=date)

session_start_time = dt.time(11, 30)
m = time_manage.Manager(session_start_time, date, subjects,
                        [c.__name__ for c in column_creation.DEFAULT_COLUMNS])

column_creation.create_stat_columns(date=get_most_recent_monday(date))
column_creation.create_subjects(subjects)
column_creation.Column.make_all(ws)

start_times = (dt.datetime(2018, 5, 5, 11, 30),
               dt.datetime(2018, 5, 5, 11, 50),
               dt.datetime(2018, 5, 5, 12, 30),
               dt.datetime(2018, 5, 5, 15, 15))

end_times = (dt.datetime(2018, 5, 5, 11, 50),
             dt.datetime(2018, 5, 5, 12, 10),
             dt.datetime(2018, 5, 5, 14, 13),
             dt.datetime(2018, 5, 5, 16, 0))

subjects = (3, 0, 5, 2)

final_end_time = end_times[-1]


for subject, start, end in zip(subjects, start_times, end_times):
    m.start_timer(subject, start)
    m.stop_timer(end)
    m.export_to_json(JSON_PATH)

date = dt.date(2018, 5, 6)
session_start_time = dt.time(19, 30)

m.write_data(ws, final_end_time)

m = time_manage.Manager.from_json(file_io.load_json(JSON_PATH),
                                  date,
                                  session_start_time)

start_times = (dt.datetime(2018, 5, 6, 19, 30),
               dt.datetime(2018, 5, 6, 20, 50),
               dt.datetime(2018, 5, 6, 23, 00),
               dt.datetime(2018, 5, 7, 0, 15),
               dt.datetime(2018, 5, 7, 2, 0))

end_times = (dt.datetime(2018, 5, 6, 20, 40),
             dt.datetime(2018, 5, 6, 22, 10),
             dt.datetime(2018, 5, 7, 0, 10),
             dt.datetime(2018, 5, 7, 1, 0),
             dt.datetime(2018, 5, 7, 3, 0))

subjects = (1, 0, 4, 5, 0)

final_end_time = end_times[-1]
for subject, start, end in zip(subjects, start_times, end_times):
    m.start_timer(subject, start)
    m.stop_timer(end)
    m.export_to_json(JSON_PATH)


m.write_data(ws, final_end_time)
file_io.save_file(wb, PATH)
