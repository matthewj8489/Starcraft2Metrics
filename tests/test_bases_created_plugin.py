import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath("..\\"))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from unittest.mock import MagicMock
    
import sc2reader
    
from metrics.sc2metric import Sc2MetricAnalyzer    
from metrics.plugins.bases_created import BasesCreatedTracker
from metrics.util import convert_gametime_to_realtime_r


class TestBasesCreatedPlugin(unittest.TestCase):               
    def setUp(self):
        self.event = MagicMock(second=0)
        self.event.unit = MagicMock(is_building=False,
                                    name = "",
                                    owner = MagicMock(pid=0))
        self.replay = MagicMock(player={1: MagicMock(), 2: MagicMock()})


    def tearDown(self):
        self.event.dispose()
        self.replay.dispose()
        
                
    def test_handleInitGame(self):
        rep = MagicMock(players=[MagicMock(), MagicMock()])
        base_track = BasesCreatedTracker()
        base_track.handleInitGame(None, rep)
        for plyr in rep.players:
            self.assertTrue(hasattr(plyr, 'metrics'))
            self.assertIsNotNone(plyr.metrics)
            self.assertIs(type(plyr.metrics), Sc2MetricAnalyzer)
            
            
    def test_handleUnitBornEvent(self):
        self.event.second = 20
        self.event.unit.is_building = False
        self.event.unit.name = "UnitBornEvent"
        self.event.owner.pid = 1
        
        base_track = BasesCreatedTracker()
        base_track.handleInitGame(None, self.replay)
        base_track.handleUnitBornEvent(self.event, self.replay)
        
        self.assertEqual(len(self.replay.player[1].metrics.bases_created), 1)
        
                
if __name__ == '__main__':
    unittest.main()