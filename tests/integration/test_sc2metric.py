import os
import sys
import json

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


import metrics
import sc2reader
from metrics.util import convert_gametime_to_realtime_r

REPLAY_DIR=os.path.join(os.path.dirname(__file__),"test_replays")

class TestMetrics(unittest.TestCase):

    def _get_json_data(self):
        json_dat = None
        with open(os.path.join(REPLAY_DIR, "replay_info.json", "r")) as fl:
            json_dat = json.load(fl)       
        
        return json_dat
        

    def test_metrics_exist(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "standard_1v1.SC2Replay"))
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
            #self.assertNotEqual(len(p1_met.current_food_used), 0)
            #self.assertNotEqual(len(p1_met.current_food_made), 0)
            self.assertNotEqual(len(p1_met.supply), 0)
            self.assertNotEqual(len(p1_met.resources), 0)
            self.assertNotEqual(p1_met.avg_apm, 0)
            
            
    def test_metrics_are_sorted(self):
        self.assertTrue(False)
        

    def test_time_to_max_created(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "standard_1v1.SC2Replay"))
        p1_met = replay.player[1].metrics
                                
        # verify by going through replay
        self.assertEqual(p1_met.time_to_supply_created(200), 613)


    def test_time_to_max_with_max_workers_created(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "standard_1v1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        # verify by going through replay
        self.assertEqual(p1_met.time_to_supply_created_max_workers(200, 75), 613)


    def test_time_to_supply_created_max_workers_with_more_than_total_supply(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "standard_1v1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        self.assertIsNone(p1_met.time_to_supply_created_max_workers(1000, 75))
        
        
    def test_time_to_X_workers(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics

        self.assertEqual(p1_met.time_to_workers_created(66), 477)
        self.assertEqual(p1_met.time_to_workers_created(75), 546)
        
        
    def test_time_to_workers_created_with_more_than_total_workers_created(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics

        self.assertIsNone(p1_met.time_to_workers_created(200))
        
        
    def test_time_to_bases(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        # verify these numbers with going through the replay
        self.assertEqual(p1_met.time_to_bases_created(1), 0)
        self.assertEqual(p1_met.time_to_bases_created(2), 163)
        self.assertEqual(p1_met.time_to_bases_created(3), 416)
        
    
    def test_time_to_bases_out_of_range(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        # test the fail cases
        self.assertIsNone(p1_met.time_to_bases_created(6))
        self.assertIsNone(p1_met.time_to_bases_created(0))
                                             

    def test_supply_capped_time(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "sc62_aur559.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        self.assertEqual(p1_met.supply_capped(), 63)
        
        replay = sc2reader.load_replay("test_replays\\pvt_macro1.SC2Replay")
        p1_met = replay.player[1].metrics
        
        self.assertEqual(p1_met.supply_capped(), 64)

        
    def test_workers_created_at_time(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        # use sc2replaystats to find values: http://sc2replaystats.com/replay/10178735
        self.assertEqual(p1_met.workers_created_at_time(441), 60)
        self.assertEqual(p1_met.workers_created_at_time(504), 70)
        self.assertEqual(p1_met.workers_created_at_time(547), 76)

    
    def test_army_created_at_time(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        # use sc2replaystats to find values: http://sc2replaystats.com/replay/10178735
        # use resources lost tab to figure out total created
        self.assertEqual(p1_met.army_created_at_time(441), 31)
        self.assertEqual(p1_met.army_created_at_time(546), 43)
    
    
    def test_supply_created_at_time(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        # use sc2replaystats to find values: http://sc2replaystats.com/replay/10178735
        # use resources lost tab to figure out total created
        self.assertEqual(p1_met.supply_created_at_time(441), 87)
        self.assertEqual(p1_met.supply_created_at_time(546), 125)
        
    
    def test_avg_sq(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        self.assertEqual(round(p1_met.avg_sq()), 105)


    def test_avg_sq_at_time(self):
        ## TODO
        #self.assertEqual(round(p1_met.avg_sq_at_time(500), 1), 110.5)
        pass


    def test_avg_sq_pre_max(self):
        ## TODO
        #self.assertEqual(round(p1_met.avg_sq_pre_max(), 1), 122.8)
        pass
            
            
    def test_aur(self):       
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        self.assertEqual(round(p1_met.aur()), 1428)


    def test_aur_at_time(self):
        ## TODO
        #self.assertEqual(round(p1_met.aur_at_time(500)), ???)
        pass


    def test_aur_pre_max(self):
        ## TODO
        #self.assertEqual(round(p1_met.aur_pre_max()), ???)
        pass
        
        
    def test_aur_pre_max_when_never_maxed(self):
        ## TODO
        #replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        #p1_met = replay.player[1].metrics
        
        #self.assertEqual(round(p1_met.aur_pre_max()), 1428)
        pass
    
        
    def test_avg_rcr(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        self.assertEqual(round(p1_met.avg_rcr()), 2491)


    def test_avg_rcr_at_time(self):
        ## TODO
        #self.assertEqual(round(p1_met.avg_rcr_at_time(500)), ???)
        pass


    def test_avg_rcr_pre_max(self):
        ## TODO
        #self.assertEqual(round(p1_met.avg_rcr_pre_max()), ???)
        pass
        
        
    def test_avg_rcr_pre_max_when_never_maxed(self):
        ## TODO
        #replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        #p1_met = replay.player[1].metrics
        
        #self.assertEqual(round(p1_met.avg_rcr()), 2491)
        pass
            
            
    def test_apm(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        self.assertEqual(round(p1_met.avg_apm), 114)
        
        
    def test_spm(self):
        replay = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        p1_met = replay.player[1].metrics
        
        self.assertEqual(round(p1_met.avg_spm, 1), 15.4)
        
            
    # def test_current_food(self):    
        # replay = sc2reader.load_replay("test_replays\\pvt_macro1.SC2Replay")
        # p1_met = replay.player[1].metrics
        
        # stats = None
        # with open("test_replays\\replay_info.json", "r") as fl:
            # stats = json.load(fl)       
        
        # if stats is None:
            # self.fail("could not open replay_info json file.")
            
        # for st in stats[0]['stats']:
            # for idx in range(0, len(st['players'])):
                # fd_md_lt = list(filter(lambda x: x.second <= st['time'], replay.players[idx].metrics.current_food_made))
                # fd_us_lt = list(filter(lambda x: x.second <= st['time'], replay.players[idx].metrics.current_food_used))
                
                # fd_md = max(fd_md_lt, key=lambda x: x.second)
                # fd_us = max(fd_us_lt, key=lambda x: x.second)
                
                # self.assertTrue(fd_md.second <= st['time'])
                # self.assertTrue(fd_us.second <= st['time'])
                
                # self.assertEqual(st['players'][idx]['supp_made'], fd_md.supply)
                # self.assertEqual(st['players'][idx]['supp_used'], fd_us.supply)
                
                   

        
        
    
if __name__ == '__main__':
    unittest.main()
