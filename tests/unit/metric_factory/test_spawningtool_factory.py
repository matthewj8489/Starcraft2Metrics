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

    def _create_mock_build(self, player_names):
        mock_build = {}
        mock_build['players'] = {}
        for nm in player_names:
            mock_build['players'][nm] = {}
            mock_build['players'][nm]['name'] = nm
            mock_build['players'][nm]['buildOrder'] = []
        return mock_build

    def _create_mock_bo_unit(self, name, supply, time_str, frame):
        return {'name': name, 'supply': supply, 'time': time_str, 'frame': frame}
        

    ########################## generateBuildOrderElements ##########################

    @patch('metrics.metric_factory.spawningtool_factory.spawningtool.parser')
    def test_build_order_elements_generated_correctly(self, spawn_parse_mock):
        mock_build = self._create_mock_build(['Faker'])
        mock_build['players']['Faker']['buildOrder'].append(self._create_mock_bo_unit('Zealot', 2, '0:10', 50))
        mock_build['players']['Faker']['buildOrder'].append(self._create_mock_bo_unit('Probe', 1, '0:30', 150))
        
        spawn_parse_mock.parse_replay.return_value = mock_build

        fact = SpawningtoolFactory(None)

        boe = fact.generateBuildOrderElements('Faker')

        self.assertEqual(2, len(boe))
        self.assertEqual(1, boe[0].build_num)
        self.assertEqual('Zealot', boe[0].name)
        self.assertEqual(2, boe[0].supply)
        self.assertEqual(10, boe[0].time)
        self.assertEqual(50, boe[0].frame)
        self.assertEqual(2, boe[1].build_num)
        self.assertEqual('Probe', boe[1].name)
        self.assertEqual(1, boe[1].supply)
        self.assertEqual(30, boe[1].time)
        self.assertEqual(150, boe[1].frame)

    @patch('metrics.metric_factory.spawningtool_factory.spawningtool.parser')
    def test_build_order_elements_correct_when_player_name_does_not_match(self, spawn_parse_mock):
        mock_build = self._create_mock_build(['Faker'])
        mock_build['players']['Faker']['buildOrder'].append(self._create_mock_bo_unit('Zealot', 2, '0:10', 50))

        spawn_parse_mock.parse_replay.return_value = mock_build

        fact = SpawningtoolFactory(None)
        boe = fact.generateBuildOrderElements('Nobody')

        self.assertEqual(0, len(boe))
        
    
    @patch('metrics.metric_factory.spawningtool_factory.spawningtool.parser')
    def test_build_order_elements_correct_when_no_elements_exist(self, spawn_parse_mock):
        mock_build = self._create_mock_build(['Faker'])
        
        spawn_parse_mock.parse_replay.return_value = mock_build

        fact = SpawningtoolFactory(None)
        boe = fact.generateBuildOrderElements('Faker')

        self.assertEqual(0, len(boe))


    @patch('metrics.metric_factory.spawningtool_factory.spawningtool.parser')
    def test_build_order_elements_correct_when_more_than_one_player(self, spawn_parse_mock):
        mock_build = self._create_mock_build(['Faker', 'Nobody'])
        mock_build['players']['Faker']['buildOrder'].append(self._create_mock_bo_unit('Zealot', 2, '0:10', 50))
        mock_build['players']['Nobody']['buildOrder'].append(self._create_mock_bo_unit('Probe', 1, '0:15', 75))

        spawn_parse_mock.parse_replay.return_value = mock_build

        fact = SpawningtoolFactory(None)
        boe = fact.generateBuildOrderElements('Faker')

        self.assertEqual(1, len(boe))
        self.assertEqual(1, boe[0].build_num)
        self.assertEqual('Zealot', boe[0].name)
        self.assertEqual(2, boe[0].supply)
        self.assertEqual(10, boe[0].time)
        self.assertEqual(50, boe[0].frame)


    ########################## generateReplayMetadata ##########################

    #@patch('metrics.metric_factory.spawningtool_factory.spawningtool.parser')
    #def test_

if __name__ == '__main__':
    unittest.main()
