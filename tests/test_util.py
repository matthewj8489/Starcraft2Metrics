import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import metrics
from metrics import plugins
from metrics.util import *
import sc2reader

REPLAY_DIR=os.path.join(os.path.dirname(__file__),"test_replays")

class TestUtil(unittest.TestCase):

    def test_gametime_to_realtime_r(self):
        rep = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        
        self.assertEqual(convert_to_realtime_r(rep, 1358), 970)
        
    def test_realtime_to_gametime_r(self):
        rep = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        
        self.assertEqual(convert_to_gametime_r(rep, 970), 1358)



if __name__ == '__main__':
    unittest.main()