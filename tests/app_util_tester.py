import re
import unittest

import pandas

from app_util import has_sequence, fetch_vehicle_make


class MyTestCase(unittest.TestCase):
    def test_something(self):
        data_frame = pandas.read_csv('../sample/sample.csv')
        self.assertGreater(len(data_frame), 0)


if __name__ == '__main__':
    unittest.main()
