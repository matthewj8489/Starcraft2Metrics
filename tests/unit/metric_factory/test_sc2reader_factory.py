import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir)))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from unittest.mock import Mock
from unittest.mock import patch

from metrics.metric_factory.sc2reader_factory import *

class TestSc2ReaderFactory(unittest.TestCase):

    @patch('metrics.metric_factory.sc2reader_factory.sc2reader')
    @patch('metrics.metric_factory.sc2reader_factory.convert_to_realtime_r')
    def test_resources_tracked_adds_resource(self, mock_sc2reader, mock_convert_to_realtime_r):
        player_name = 'Faker'
        mock_replay = Mock()
        mock_replay.players = []
        mock_replay.players.append(Mock())
        mock_replay.players[0].name = player_name
        mock_replay.players[0].events = []
        mock_replay.players[0].events.append(Mock())
        mock_replay.players[0].events[0].return_value = {
            'name': 'PlayerStatsEvent',
            'second': 10,
            'minerals_collection_rate': 1000,
            'vespene_collection_rate': 200,
            'minerals_current': 150,
            'vespene_current': 100
        }
        
        mock_sc2reader.load_replay.return_value = mock_replay
        mock_convert_to_realtime_r.return_value = 10

        sc2_fact = Sc2ReaderFactory("")
        res = sc2_fact.generateResourcesTracked(player_name)

        mock_sc2reader.players[0].assert_called()
        mock_sc2reader.players[0].name.assert_called()

        self.assertEqual(1, len(res))
        self.assertEqual(10, res.second)
        self.assertEqual(1200, res.res_col)
        self.assertEqual(250, res.res_unspent)


if __name__ == '__main__':
    unittest.main()



