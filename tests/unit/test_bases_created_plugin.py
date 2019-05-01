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
from metrics.plugins.bases_created import BasesCreatedTracker


class TestBasesCreatedPlugin(unittest.TestCase):
    
    
    def _generate_stub_event(self):
        event = MagicMock(second=0)
        event.unit = MagicMock(is_building=False,
                               name = "",
                               owner = MagicMock(pid=0))
        return event
        
    
    def _generate_stub_replay(self):
        replay = MagicMock(player={1: MagicMock(), 2: MagicMock()},
                           game_length = MagicMock(seconds=100),
                           game_fps = 16,
                           frames = 500)
        replay.players = [replay.player[1], replay.player[2]]
        
        return replay

    
    def _initialize_event_and_bases_created_tracker(self, replay, event, bases_created_tracker):
        event.second = 20
        event.unit.owner.pid = 1
        event.unit.name = "Nexus"
        event.unit.is_building = True
        
        bases_created_tracker.handleInitGame(None, replay)        
        
                
    def test_handleInitGame(self):
        rep = MagicMock(players=[MagicMock(), MagicMock()])
        base_track = BasesCreatedTracker()
        base_track.handleInitGame(None, rep)
        for plyr in rep.players:
            self.assertTrue(hasattr(plyr, 'metrics'))
            self.assertIsNotNone(plyr.metrics)
            self.assertIs(type(plyr.metrics), Sc2MetricAnalyzer)
            
            
    def test_handleUnitBornEvent_with_building_event(self):      
        for base_name in ['Nexus', 'CommandCenter', 'Hatchery']:
            with self.subTest(base_name=base_name):
                base_track = BasesCreatedTracker()
                event = self._generate_stub_event()
                replay = self._generate_stub_replay()
                
                self._initialize_event_and_bases_created_tracker(replay, event, base_track)
                event.unit.is_building = True
                event.unit.name = base_name
                
                base_track.handleUnitBornEvent(event, replay)
        
                self.assertEqual(len(replay.player[1].metrics.bases_created), 1)
    

    def test_handleUnitBornEvent_with_non_building_event(self):
        base_track = BasesCreatedTracker()
        event = self._generate_stub_event()
        replay = self._generate_stub_replay()
        
        self._initialize_event_and_bases_created_tracker(replay, event, base_track)
        event.unit.is_building = False
        event.unit.name = "Probe"
                
        base_track.handleUnitBornEvent(event, replay)
        
        self.assertEqual(len(replay.player[1].metrics.bases_created), 0)
        
        
    def test_handleUnitBornEvent_with_nonbase_building(self):
        base_track = BasesCreatedTracker()
        event = self._generate_stub_event()
        replay = self._generate_stub_replay()
        
        self._initialize_event_and_bases_created_tracker(replay, event, base_track)
        event.unit.is_building = True
        event.unit.name = "Pylon"
                
        base_track.handleUnitBornEvent(event, replay)
        
        self.assertEqual(len(replay.player[1].metrics.bases_created), 0)
        
                
    def test_handleUnitDoneEvent_with_building_event(self):
        for base_name in ['Nexus', 'CommandCenter', 'Hatchery']:
            with self.subTest(base_name=base_name):
                base_track = BasesCreatedTracker()
                event = self._generate_stub_event()
                replay = self._generate_stub_replay()
                
                self._initialize_event_and_bases_created_tracker(replay, event, base_track)
                event.unit.is_building = True
                event.unit.name = base_name
                
                base_track.handleUnitDoneEvent(event, replay)
        
                self.assertEqual(len(replay.player[1].metrics.bases_created), 1)
    

    def test_handleUnitDoneEvent_with_non_building_event(self):
        base_track = BasesCreatedTracker()
        event = self._generate_stub_event()
        replay = self._generate_stub_replay()
        
        self._initialize_event_and_bases_created_tracker(replay, event, base_track)
        event.unit.is_building = False
        event.unit.name = "Probe"
                
        base_track.handleUnitDoneEvent(event, replay)
        
        self.assertEqual(len(replay.player[1].metrics.bases_created), 0)
        
        
    def test_handleUnitDoneEvent_with_nonbase_building(self):
        base_track = BasesCreatedTracker()
        event = self._generate_stub_event()
        replay = self._generate_stub_replay()
        
        self._initialize_event_and_bases_created_tracker(replay, event, base_track)
        event.unit.is_building = True
        event.unit.name = "Pylon"
                
        base_track.handleUnitDoneEvent(event, replay)
        
        self.assertEqual(len(replay.player[1].metrics.bases_created), 0)
        
        
                
if __name__ == '__main__':
    unittest.main()
