import re
import unittest

import pandas

from app_util import has_sequence, fetch_vehicle_make


class MyTestCase(unittest.TestCase):
    def test_something(self):
        data_frame = pandas.read_csv('sample/sample.csv')
        for index, row in data_frame.iterrows():
            print("checking: ", row['description'])
            print(fetch_vehicle_make(row['description']))
            print(re.findall(r"(?:[\d\.\,]{1,})",row['description']))
        self.assertEqual(True, len(data_frame) > 0)


if __name__ == '__main__':
    unittest.main()
