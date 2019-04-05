import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath("..\\"))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import sc2reader
    
from metrics.plugins import BasesCreatedTracker
from metrics.util import convert_gametime_to_realtime_r


class TestBasesCreatedPlugin(unittest.TestCase):

    def test_handleInitGame(self):
        reps = sc2reader.load_replays("test_replays")
        base_track = BasesCreatedTracker()
        for rep in reps:
            self.assertFalse(hasattr(rep.players[0], 'metrics'))
            base_track.handleInitGame(None, rep)
            for plyr in rep.players:
                self.assertTrue(hasattr(plyr, 'metrics'))
                self.assertIsNotNone(plyr.metrics)
                
                
if __name__ == '__main__':
    unittest.main()