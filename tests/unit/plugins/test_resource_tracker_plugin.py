import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from unittest.mock import MagicMock
       
from metrics.sc2metric import Sc2MetricAnalyzer    
from metrics.plugins.resources import ResourceTracker


class TestResourceTrackerPlugin(unittest.TestCase):

    def _generate_stub_event(self):
        event = MagicMock(second=0,
                          pid=1,
                          minerals_collection_rate=0,
                          vespene_collection_rate=0,
                          minerals_current=0,
                          vespene_current=0)
        
        return event
        
    
    def _generate_stub_replay(self):
        replay = MagicMock(player={1: MagicMock(), 2: MagicMock()},
                           game_length = MagicMock(seconds=100),
                           game_fps = 16,
                           frames = 500)
        replay.players = [replay.player[1], replay.player[2]]
        
        return replay
        
        
    def _initialize_event_and_res_tracker(self, replay, event, res_tracker):
        event.second = 20
        event.minerals_collection_rate=800
        event.vespene_collection_rate=200
        event.minerals_current=300
        event.vespene_current=50
        
        res_tracker.handleInitGame(None, replay)        
        
                
    def test_handleInitGame(self):
        rep = MagicMock(players=[MagicMock(), MagicMock()])
        res_track = ResourceTracker()
        res_track.handleInitGame(None, rep)
        for plyr in rep.players:
            self.assertTrue(hasattr(plyr, 'metrics'))
            self.assertIsNotNone(plyr.metrics)
            self.assertIs(type(plyr.metrics), Sc2MetricAnalyzer)
            
            
    def test_handlePlayerStatsEvent_add_resource(self):
        res_track = ResourceTracker()
        event = self._generate_stub_event()
        replay = self._generate_stub_replay()
        
        self._initialize_event_and_res_tracker(replay, event, res_track)
        
        res_track.handlePlayerStatsEvent(event, replay)
        
        self.assertEqual(len(replay.player[1].metrics.resources), 1)
        
        
if __name__ == '__main__':
    unittest.main()        
