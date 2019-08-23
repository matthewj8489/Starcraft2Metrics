import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir)))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, 'metrics')))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from unittest.mock import MagicMock
from unittest.mock import patch


from metrics.metric_factory.spawningtool_factory import *

class TestSpawningToolFactory(unittest.TestCase):

    @patch('metrics.metric_factory.spawningtool_factory.spawningtool.parser')
    def test_build_order_elements_generated_correctly(self, spawn_parse_mock):
        mock_bo_unit = {'name': 'Zealot', 'supply': 2, 'time': '0:10', 'frame': 50}
        mock_build = {}
        mock_build['players'] = {}
        mock_build['players']['Faker'] = {}
        mock_build['players']['Faker']['name'] = 'Faker'
        mock_build['players']['Faker']['buildOrder'] = []
        mock_build['players']['Faker']['buildOrder'].append(mock_bo_unit)
        
        spawn_parse_mock.parse_replay.return_value = mock_build

        fact = SpawningtoolFactory(None)

        boe = fact.generateBuildOrderElements('Faker')

        self.assertEqual(1, len(boe))
        self.assertEqual(1, boe[0].build_num)
        self.assertEqual('Zealot', boe[0].name)
        self.assertEqual(2, boe[0].supply)
        self.assertEqual(10, boe[0].time)
        self.assertEqual(50, boe[0].frame)
        

if __name__ == '__main__':
    unittest.main()
