import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath("..\\"))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import metrics
from metrics import plugins
from metrics.util import convert_gametime_to_realtime_r
import sc2reader


class TestPlugins(unittest.TestCase):

    def test_resource_tracker(self):
        replay = sc2reader.load_replay("test_replays\\standard_1v1.SC2Replay")
        
        for plyr in replay.players:
            pse = list(filter(lambda x: x.name == 'PlayerStatsEvent' and x.pid == plyr.pid, replay.events))
        
            mets = plyr.metrics.resources
            self.assertEqual(len(pse), len(mets))
            for idx in range(0, len(mets)):
                self.assertEqual(convert_gametime_to_realtime_r(replay, pse[idx].second), mets[idx].second)
                self.assertEqual(pse[idx].minerals_collection_rate + pse[idx].vespene_collection_rate, mets[idx].res_col)
                self.assertEqual(pse[idx].minerals_current + pse[idx].vespene_current, mets[idx].res_unspent)
            
        
if __name__ == '__main__':
    unittest.main()