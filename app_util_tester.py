import re
import unittest

import pandas

from app_util import has_sequence


class MyTestCase(unittest.TestCase):
    def test_something(self):
        data_frame = pandas.read_csv('sample/sample.csv')
        for index, row in data_frame.iterrows():
            # link_numbers = has_sequence(row['description'] + " ")
            print("checking: ", row['description'])
            print(re.findall(r"(?:[\d\.\,]{1,})",row['description']))
        self.assertEqual(True, len(data_frame) > 0)


if __name__ == '__main__':
    unittest.main()
