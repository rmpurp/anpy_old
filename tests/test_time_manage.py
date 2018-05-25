import unittest
from anpy_lib import time_manage
import datetime as dt
import json


class TestManager(unittest.TestCase):
    def test_timer(self):
        timer = time_manage.Timer(3)
        time1 = dt.datetime(2014, 12, 4, 3, 0)
        time2 = dt.datetime(2014, 12, 4, 3, 6, 30)
        timer.start(time1)
        timer.stop(time2)
        self.assertEqual(timer.get_seconds_elapsed(), 30 + 6 * 60)

    def test_timer_from_json(self):
        json_str = '{"current_sub_idx": 3, "timer_start": 1415763004}'
        timer = time_manage.Timer.from_json(json.loads(json_str))
        time = dt.datetime(2014, 11, 12, 3, 30, 4, tzinfo=dt.timezone.utc)
        subject = 3
        self.assertEqual(timer.subject_idx, subject)
        self.assertEqual(time, timer.timer_start.astimezone(dt.timezone.utc))

    def test_timer_consistency(self):
        time = dt.datetime(2015, 6, 14, 16, 5, 30)
        time2 = dt.datetime(2015, 6, 24, 16, 5, 30)
        timer = time_manage.Timer(1)
        timer2 = time_manage.Timer(2)
        timer.start(time)
        timer2.start(time2)
        self.assertNotEqual(timer, timer2)

        json_str = json.dumps(timer.prepare_json())
        timer2 = time_manage.Timer.from_json(json.loads(json_str))
        self.assertEqual(timer, timer2)

    def test_manager(self):
        session_start = dt.time(14, 24)
        date = dt.date(2017, 4, 21)
        subjects = 'test1 test2 test3'.split(' ')
        m = time_manage.Manager(session_start, date, subjects, ['DateColumn'])
        self.assertEqual(m.time_records, [0, 0, 0])

        start_time = dt.datetime(2017, 4, 21, 14, 25, 10)
        end_time = dt.datetime(2017, 4, 21, 15, 20, 11)
        m.start_timer(1, start_time)
        m.stop_timer(end_time)
        self.assertEqual(list(map(int, m.time_records)),
                         list(map(int, [0, (1 + 55 * 60) / 60, 0])))
        start_time = dt.datetime(2017, 4, 21, 14, 25, 10)
        end_time = dt.datetime(2017, 4, 21, 16, 20, 11)
        m.start_timer(2, start_time)
        m.stop_timer(end_time)
        self.assertEqual(list(map(int, m.time_records)),
                         list(map(int, [0, (1 + 55 * 60) / 60,
                                        (1 + 115 * 60) / 60])))

    def test_manager_json(self):
        json_str = '{"session_start": [15, 41], "date": [2014, 12, 4],' \
            + '"subjects": ["suba", "subb"], "columns": ["DateColumn"],' \
            + '"time_records": [12, 14],' \
            + '"timer_running": true, "current_sub_idx": 1,' \
            + '"timer_start": 1415763004}'
        m = time_manage.Manager.from_json(json.loads(json_str))
        m2 = time_manage.Manager(dt.time(15, 41), dt.date(2014, 12, 4),
                                 ['suba', 'subb'], ['DateColumn'], [12, 14])
        m2.start_timer(1, dt.datetime.fromtimestamp(1415763004))
        self.assertEqual(m, m2)

    def test_manager_consistency(self):
        def check_consistent(manager):
            json_str = json.dumps(manager.prepare_json())
            decoded = json.loads(json_str)
            self.assertEqual(manager, time_manage.Manager.from_json(decoded))
        m = time_manage.Manager(dt.time(21, 20),
                                dt.date(2008, 5, 2),
                                ['banana', 'apple', 'dessert'],
                                ['DateColumn'],
                                [3, 4, 5])
        m2 = time_manage.Manager(dt.time(21, 20),
                                 dt.date(2008, 5, 2),
                                 ['banana', 'apple', 'dessert'],
                                 ['DateColumn'],
                                 [3, 4, 5])
        check_consistent(m)
        m.start_timer(2)
        self.assertNotEqual(m, m2)
        check_consistent(m)
        m.stop_timer()
        self.assertNotEqual(m, m2)
        check_consistent(m)


if __name__ == '__main__':
    unittest.main()
