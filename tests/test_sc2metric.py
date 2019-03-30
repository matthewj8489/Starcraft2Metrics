import os
import sys
import json

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath("..\\"))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


import metrics
import sc2reader
from metrics.util import convert_gametime_to_realtime_r

class TestMetrics(unittest.TestCase):

    def test_metrics_exist(self):
        replay = sc2reader.load_replay("test_replays\\standard_1v1.SC2Replay")
        p1_met = None
        
        # Test first metrics is part of the player
        try:
            p1_met = replay.player[1].metrics
        except:
            self.fail("metrics is not a member of the player object.")

        # Test that the instance was created
        self.assertIsNotNone(p1_met)

        # Test that data was put into the class properties
        if p1_met is not None:
            self.assertNotEqual(len(p1_met.army_created), 0)
            self.assertNotEqual(len(p1_met.workers_created), 0)
            self.assertNotEqual(len(p1_met.supply_created), 0)
            self.assertNotEqual(len(p1_met.bases_created), 0)
            self.assertNotEqual(len(p1_met.current_food_used), 0)
            self.assertNotEqual(len(p1_met.current_food_made), 0)
            self.assertNotEqual(len(p1_met.resources), 0)
            self.assertNotEqual(p1_met.avg_apm, 0)
            

    def test_time_to_max(self):
        replay = sc2reader.load_replay("test_replays\\standard_1v1.SC2Replay")
        p1_met = replay.player[1].metrics
                                
        self.assertEqual(p1_met.time_to_supply_created(200), 618)
        self.assertEqual(p1_met.time_to_supply_created_max_workers(200, 75), 618)


    def test_time_to_X_workers(self):
        #:TODO
        replay = sc2reader.load_replay("test_replays\\standard_1v1.SC2Replay")
        p1_met = replay.player[1].metrics

        self.assertEqual(p1_met.time_to_workers_created(66), 500)
        self.assertEqual(p1_met.time_to_workers_created(75), 612)


    def test_avg_sq(self):
        #: TODO
        replay = sc2reader.load_replay("test_replays\\pvt_macro2.SC2Replay")
        p1_met = replay.player[1].metrics
        
        stats = None
        with open("test_replays\\replay_info.json", "r") as fl:
            stats = json.load(fl)       
        
        if stats is None:
            self.fail("could not open replay_info json file.")
            
            
    def test_current_food(self):    
        replay = sc2reader.load_replay("test_replays\\pvt_macro2.SC2Replay")
        p1_met = replay.player[1].metrics
        
        stats = None
        with open("test_replays\\replay_info.json", "r") as fl:
            stats = json.load(fl)       
        
        if stats is None:
            self.fail("could not open replay_info json file.")
            
        for st in stats['stats']:
            for idx in range(0, len(st['players'])):
                fd_md_lt = list(filter(lambda x: x.second <= st['time'], replay.players[idx].metrics.current_food_made))
                fd_us_lt = list(filter(lambda x: x.second <= st['time'], replay.players[idx].metrics.current_food_used))
                
                fd_md = max(fd_md_lt, key=lambda x: x.second)
                fd_us = max(fd_us_lt, key=lambda x: x.second)
                
                self.assertTrue(fd_md.second <= st['time'])
                self.assertTrue(fd_us.second <= st['time'])
                
                self.assertEqual(st['players'][idx]['supp_made'], fd_md.supply)
                self.assertEqual(st['players'][idx]['supp_used'], fd_us.supply)
                
                
        
    def test_time_to_bases(self):
        replay = sc2reader.load_replay("test_replays\\pvt_macro2.SC2Replay")

        stats = None
        with open("test_replays\\replay_info.json", "r") as fl:
            stats = json.load(fl)       
        
        if stats is None:
            self.fail("could not open replay_info json file.")
            
        for bs in stats['bases']:
            for idx in range(0, len(bs['players'])):
                met = replay.players[idx].metrics
                bc = bs['players'][idx]['bases_created']
                
                for bdx in range(0, len(bc)):
                    self.assertEqual(met.time_to_bases_created(bdx+1), bc[bdx])
                                             

if __name__ == '__main__':
    unittest.main()
