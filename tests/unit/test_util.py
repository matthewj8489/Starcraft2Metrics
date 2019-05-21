import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from unittest.mock import MagicMock

import metrics
from metrics.util import *


class TestUtil(unittest.TestCase):

    
    def _generate_stub_replay(self):
        replay = MagicMock(player={1: MagicMock(), 2: MagicMock()},
                           game_length = MagicMock(seconds=100),
                           game_fps = 1,
                           frames = 100)
        replay.players = [replay.player[1], replay.player[2]]
        
        return replay
        

    def test_convert_to_gametime_r(self):
        replay = self._generate_stub_replay()
        
        # settings so that game_time == real_time
        replay.game_length.seconds = 100
        replay.game_fps = 1
        replay.frames = 100
        
        game_time = convert_to_gametime_r(replay, 10)
        
        self.assertEqual(game_time, 10)
        
        
    def test_convert_to_realtime_r(self):
        replay = self._generate_stub_replay()
        
        # settings so that game_time == real_time
        replay.game_length.seconds = 100
        replay.game_fps = 1
        replay.frames = 100
        
        real_time = convert_to_realtime_r(replay, 10)
        
        self.assertEqual(real_time, 10)
        
        
if __name__ == '__main__':
    unittest.main()
        
