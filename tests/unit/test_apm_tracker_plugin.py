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
from metrics.plugins.apm import APMTracker


class TestAPMTrackerPlugin(unittest.TestCase):

    def _generate_stub_event(self):
        event = MagicMock(second=0)
        event.player = MagicMock(pid=0)

        return event
        
    
    def _generate_stub_replay(self):
        replay = MagicMock(player={1: MagicMock(pid=1), 2: MagicMock(pid=2)},
                           game_length = MagicMock(seconds=100),
                           game_fps = 1,
                           frames = 100) # this will set everything up so that 1 game sec = 1 real sec
        replay.players = [replay.player[1], replay.player[2]]
        
        return replay
        
    
    def _initialize_event_and_apm_tracker(self, replay, event, apm_tracker):
        event.second = 20
        event.player.pid = 1
        
        apm_tracker.handleInitGame(None, replay)
        
        
    def test_handleInitGame(self):
        rep = MagicMock(players=[MagicMock(), MagicMock()])
        apm_track = APMTracker()
        apm_track.handleInitGame(None, rep)
        for plyr in rep.players:
            self.assertTrue(hasattr(plyr, 'metrics'))
            self.assertIsNotNone(plyr.metrics)
            self.assertIs(type(plyr.metrics), Sc2MetricAnalyzer)
        
    
    def test_correct_apm_when_no_events_fire(self):
        apm = APMTracker()
        event = self._generate_stub_event()
        replay = self._generate_stub_replay()
        
        self._initialize_event_and_apm_tracker(replay, event, apm)
        
        apm.handleInitGame(event, replay)
        apm.handlePlayerLeaveEvent(event, replay)
        apm.handleEndGame(event, replay)
        
        self.assertEqual(replay.player[1].metrics.avg_apm, 0)
        
        
    def test_correct_apm_when_ControlGroupEvent_is_fired(self):
        apm = APMTracker()
        event = self._generate_stub_event()
        replay = self._generate_stub_replay()
        
        self._initialize_event_and_apm_tracker(replay, event, apm)
        
        apm.handleInitGame(event, replay)
        event.second = 20
        apm.handleControlGroupEvent(event, replay)
        event.second = 60
        apm.handlePlayerLeaveEvent(event, replay)
        apm.handleEndGame(event, replay)
        
        self.assertEqual(replay.player[1].metrics.avg_apm, 1)
        
        
    def test_correct_apm_when_SelectionEvent_is_fired(self):
        apm = APMTracker()
        event = self._generate_stub_event()
        replay = self._generate_stub_replay()
        
        self._initialize_event_and_apm_tracker(replay, event, apm)
        
        apm.handleInitGame(event, replay)
        event.second = 20
        apm.handleSelectionEvent(event, replay)
        event.second = 60
        apm.handlePlayerLeaveEvent(event, replay)
        apm.handleEndGame(event, replay)
        
        self.assertEqual(replay.player[1].metrics.avg_apm, 1)
     

    def test_correct_apm_when_CommandEvent_is_fired(self):
        apm = APMTracker()
        event = self._generate_stub_event()
        replay = self._generate_stub_replay()
        
        self._initialize_event_and_apm_tracker(replay, event, apm)
        
        apm.handleInitGame(event, replay)
        event.second = 20
        apm.handleCommandEvent(event, replay)
        event.second = 60
        apm.handlePlayerLeaveEvent(event, replay)
        apm.handleEndGame(event, replay)
        
        self.assertEqual(replay.player[1].metrics.avg_apm, 1)
        
    
    def test_correct_apm_when_multiple_events_are_fired(self):
        apm = APMTracker()
        event = self._generate_stub_event()
        replay = self._generate_stub_replay()
        
        self._initialize_event_and_apm_tracker(replay, event, apm)
        
        apm.handleInitGame(event, replay)
        event.second = 20
        apm.handleControlGroupEvent(event, replay)
        event.second = 40
        apm.handleSelectionEvent(event, replay)
        event.second = 80
        apm.handleCommandEvent(event, replay)
        event.second = 120
        apm.handlePlayerLeaveEvent(event, replay)
        apm.handleEndGame(event, replay)
        
        self.assertEqual(replay.player[1].metrics.avg_apm, 1.5)
        
if __name__ == '__main__':
    unittest.main()        