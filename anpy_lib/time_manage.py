import datetime as dt
from anpy_lib.utils import date_to_tuple
from anpy_lib.utils import time_to_tuple
from typing import Optional


class Manager:
    def __init__(self,
                 session_start: dt.time,
                 date: dt.date,
                 subjects,
                 time_records=None):
        self.subjects = list(subjects)
        self.date = date
        if not time_records:
            self.time_records = [0] * len(subjects)
        else:
            assert len(time_records) == len(subjects)
            self.time_records = time_records
        self.session_start = session_start
        self.timer = None

    def prepare_json(self):
        keys = ('session_start', 'date', 'subjects',
                'time_records', 'timer_running')
        timer_running = bool(self.timer)
        values = (time_to_tuple(self.session_start), date_to_tuple(self.date),
                  self.subjects, self.time_records, timer_running)
        result = dict(zip(keys, values))
        if timer_running:
            result.update(self.timer.prepare_json())
        return result

    def start_timer(self, sub_idx, timer_start: Optional[dt.datetime] = None):
        assert not self.timer, "Timer has already started"
        self.timer = Timer(sub_idx, timer_start)

    def stop_timer(self, time=None):
        assert self.timer, "Timer has not been started"
        time_elapsed = self.timer.get_seconds_elapsed(time)
        self.time_records[self.timer.subject_idx] = time_elapsed / 60
        self.timer = None

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    @staticmethod
    def from_json(decoded):
        manager = Manager(dt.time(*decoded['session_start']),
                          dt.date(*decoded['date']),
                          list(decoded['subjects']),
                          list(decoded['time_records']))
        if decoded['timer_running']:
            manager.timer = Timer.from_json(decoded)
        return manager


class Timer:
    def __init__(self, subject_idx, timer_start: Optional[dt.datetime] = None):
        self.subject_idx = subject_idx
        self.start(timer_start)
        self.timer_stop = None

    def start(self, time=None):
        if not time:
            time = dt.datetime.now()
        assert time is not None
        self.timer_start = time

    def stop(self, time=None):
        if not time:
            time = dt.datetime.now()
        assert time is not None
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
        keys = ('current_sub_idx', 'timer_start')
        vals = (self.subject_idx, self.timer_start.timestamp())
        return dict(zip(keys, vals))

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False

    @staticmethod
    def from_json(decoded):
        timer = Timer(decoded['current_sub_idx'],
                      dt.datetime.fromtimestamp(decoded['timer_start']))
        return timer
