import datetime as dt
from anpy_lib.utils import date_to_tuple
from anpy_lib.utils import time_to_tuple
from typing import Optional


class Manager:
    def __init__(time_start: dt.time,
                 date: dt.date,
                 subjects,
                 time_records=None):
        self.subjects = subjects
        if not time_records:
            self.time_records = [0] * len(subjects)
        else:
            assert len(time_records) == len(subjects)
            self.time_records = time_records
        self.time_start = time_start
        self.timer = None

    def prepare_json(self):
        keys = ('time_start', 'date', 'subjects',
                'time_records', 'timer_running')
        timer_running = self.timer is not None
        values = (time_to_tuple(time_start), date_to_tuple(date), subjects,
                  time_records, timer_running)
        result = dict(zip(keys, values))
        if timer_running:
            result.update(self.timer.prepare_json())

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    @staticmethod
    def from_json(decoded):
        manager = Manager(decoded['time_start'],
                          decoded['date'],
                          decoded['subjects'],
                          decoded['time_records'])
        if decoded['timer_running']:
            timer = Timer.from_json(decoded)
        return manager


class Timer:
    def __init__(self, subject, timer_start: Optional[dt.datetime]=None):
        self.subject = subject
        self.timer_start = timer_start
        self.timer_stop = None

    def start(self, time=None):
        if not time:
            time = dt.datetime.now()
        self.timer_start = time

    def stop(self, time=None):
        if not time:
            time = dt.datetime.now()
        self.timer_stop = time

    def get_seconds_elapsed(self, time_end=None):
        if not time_end:
            time_end = self.timer_stop
        if not time_end:
            time_end = dt.datetime.now()
        return (time_end - self.timer_start).seconds

    def prepare_json(self):
        if self.timer_stop:
            return dict()
        keys = ('current_subject', 'timer_start')
        vals = (self.subject, self.timer_start.timestamp())
        return dict(zip(keys, vals))

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    @staticmethod
    def from_json(decoded):
        timer = Timer(decoded['current_subject'],
                      dt.datetime.fromtimestamp(decoded['timer_start']))
        return timer
