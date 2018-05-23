import unittest
from anpy_lib import time_manage
import datetime as dt
import json

class TestManager(unittest.TestCase):
    def test_timer(self):
        timer = time_manage.Timer("Test Subject")
        time1 = dt.datetime(2014, 12, 4, 3, 0)
        time2 = dt.datetime(2014, 12, 4, 3, 6, 30)
        timer.start(time1)
        timer.stop(time2)
        self.assertEqual(timer.get_seconds_elapsed(), 30 + 6 * 60)

    def test_timer_from_json(self):
        json_str = '{"current_subject": "ap_bio", "timer_start": 1415763004}'
        timer = time_manage.Timer.from_json(json.loads(json_str))
        time = dt.datetime(2014, 11, 12, 3, 30, 4, tzinfo=dt.timezone.utc)
        subject = 'ap_bio'
        self.assertEqual(timer.subject, subject)
        self.assertEqual(time, timer.timer_start.astimezone(dt.timezone.utc))

    def test_timer_consistency(self):
        time = dt.datetime(2015, 6, 14, 16, 5, 30)
        time2 = dt.datetime(2015, 6, 24, 16, 5, 30)
        timer = time_manage.Timer("Subject 1")
        timer2 = time_manage.Timer("Subject 2")
        timer.start(time)
        timer2.start(time2)
        self.assertNotEqual(timer, timer2)

        json_str = json.dumps(timer.prepare_json())
        timer2 = time_manage.Timer.from_json(json.loads(json_str))
        self.assertEqual(timer, timer2)

if __name__ == '__main__':
    unittest.main()
