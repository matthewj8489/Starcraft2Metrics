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
        reps = sc2reader.load_replays("test_replays")
        for rep in reps:
            for plyr in rep.players:
                pse = list(filter(lambda x: x.name == 'PlayerStatsEvent' and x.pid == plyr.pid, rep.events))
                
                mets = plyr.metrics.resources
                self.assertEqual(len(pse), len(mets))
                for idx in range(0, len(mets)):
                    self.assertEqual(convert_gametime_to_realtime_r(rep, pse[idx].second), mets[idx].second)
                    self.assertEqual(pse[idx].minerals_collection_rate + pse[idx].vespene_collection_rate, mets[idx].res_col)
                    self.assertEqual(pse[idx].minerals_current + pse[idx].vespene_current, mets[idx].res_unspent)
    
    
    def test_bases_created_tracker(self):
        base_names = ['Nexus', 'CommandCenter', 'Hatchery']
        reps = sc2reader.load_replays("test_replays")
        for rep in reps:
            for plyr in rep.players:
                ube = list(filter(lambda x: x.name == 'UnitBornEvent' and 
                                            x.unit.is_building and
                                            x.unit.name in base_names and
                                            x.unit.owner.pid == plyr.pid, rep.events))
                ude = list(filter(lambda x: x.name == 'UnitDoneEvent' and
                                            x.unit.is_building and
                                            x.unit.name in base_names and
                                            x.unit.owner.pid == plyr.pid, rep.events))
                
                evts = sorted(ube+ude, key=lambda x: x.second)
                mets = plyr.metrics.bases_created
                self.assertEqual(len(evts), len(mets))
                for idx in range(0, len(mets)):
                    self.assertEqual(convert_gametime_to_realtime_r(rep,evts[idx].second), mets[idx].second)

        
if __name__ == '__main__':
    unittest.main()