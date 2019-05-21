import os
import sys
import json

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import metrics
from metrics import plugins
from metrics.util import convert_to_realtime_r
import sc2reader

REPLAY_DIR=os.path.join(os.path.dirname(__file__),"integration\\test_replays")

class TestPlugins(unittest.TestCase):

    def test_time_converter(self):
        rep = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))
        
        self.assertIsNotNone(rep.game_to_real_time_multiplier)
        self.assertIsNotNone(rep.real_to_game_time_multiplier)

        # check that the multipliers can convert a gametime to a real time and
        # vice-versa
        

    def test_supply_tracker_correct_supply_with_no_archons(self):
        pass


    def test_supply_tracker_correct_supply_with_dt_archons(self):
        pass


    def test_supply_tracker_correct_supply_with_ht_archons(self):
        rep = sc2reader.load_replay(os.path.join(REPLAY_DIR, "pvt_macro1.SC2Replay"))

        # check that the supply made and supply used at a given second is correct to what
        # is observed in a replay
        sup = rep.player[1].metrics.supply

        # 9:34 - 139/141
        filt = list(filter(lambda x: x.second <= 574, sup))
        self.assertTrue(len(filt) > 0)
        
        sup_check = filt[len(filt)-1]
        self.assertEqual(sup_check.supply_used, 139)#135
        self.assertEqual(sup_check.supply_made, 141)

        # 12:29 - 150/188
        filt = list(filter(lambda x: x.second <= 749, sup))
        self.assertTrue(len(filt) > 0)
        
        sup_check = filt[len(filt)-1]
        self.assertEqual(sup_check.supply_used, 150)#146
        self.assertEqual(sup_check.supply_made, 188)

        # 13:46 - 197/200
        filt = list(filter(lambda x: x.second <= 826, sup))
        self.assertTrue(len(filt) > 0)
        
        sup_check = filt[len(filt)-1]
        self.assertEqual(sup_check.supply_used, 197)#215
        self.assertEqual(sup_check.supply_made, 204)

        # 15:45 - 174/200
        filt = list(filter(lambda x: x.second <= 945, sup))
        self.assertTrue(len(filt) > 0)
        
        sup_check = filt[len(filt)-1]
        self.assertEqual(sup_check.supply_used, 174)#164
        self.assertEqual(sup_check.supply_made, 235)
        


    def test_supply_tracker_correct_supply_with_dt_and_ht_archons(self):
        pass
        
        
    def test_supply_tracker_with_hallucinated_units(self):
        # There is a bug with sc2metric where units created during unit born events do not have
        # the 'hallucinated' member filled out correctly and will always appear as not
        # hallucinated. 
        # This replay has only sentries and probes being created, while all other
        # units are hallucinated.
        # create 15 sentries then start making all hallucinated units after - no more sentries
        # supply before hallucinations: 75 : 30 army supply, 45 workers
        # first hallucinated units are made at 5:38 - 3 probes
                
        rep = sc2reader.load_replay(os.path.join(REPLAY_DIR, "sentry_hallucinate.SC2Replay"))
        
        met = rep.player[1].metrics
        sup = rep.player[1].metrics.supply


        self.assertEqual(met.first_time_to_supply(80), -1) # never get to 80 supply
        self.assertEqual(met.time_to_supply_created(80), 332) # time of last real unit made
        self.assertEqual(met.supply_created_at_time(390), 75) # supply should be 75 for the rest of the game
        

##    def test_resource_tracker_against_sc2reader(self): 
##        reps = sc2reader.load_replays(REPLAY_DIR)
##        for rep in reps:
##            for plyr in rep.players:
##                pse = list(filter(lambda x: x.name == 'PlayerStatsEvent' and x.pid == plyr.pid, rep.events))
##                
##                mets = plyr.metrics.resources
##                self.assertEqual(len(pse), len(mets))
##                for idx in range(0, len(mets)):
##                    self.assertEqual(convert_to_realtime_r(rep, pse[idx].second), mets[idx].second)
##                    self.assertEqual(pse[idx].minerals_collection_rate + pse[idx].vespene_collection_rate, mets[idx].res_col)
##                    self.assertEqual(pse[idx].minerals_current + pse[idx].vespene_current, mets[idx].res_unspent)
##    
##    
##    def test_resource_tracker_against_json_data(self):
##        #: TODO
##        pass
##    
##    
##    def test_bases_created_tracker_against_sc2reader(self):
##        base_names = ['Nexus', 'CommandCenter', 'Hatchery']
##        reps = sc2reader.load_replays(REPLAY_DIR)
##        for rep in reps:
##            for plyr in rep.players:
##                ube = list(filter(lambda x: x.name == 'UnitBornEvent' and 
##                                            x.unit.is_building and
##                                            x.unit.name in base_names and
##                                            x.unit.owner.pid == plyr.pid, rep.events))
##                ude = list(filter(lambda x: x.name == 'UnitDoneEvent' and
##                                            x.unit.is_building and
##                                            x.unit.name in base_names and
##                                            x.unit.owner.pid == plyr.pid, rep.events))
##                
##                evts = sorted(ube+ude, key=lambda x: x.second)
##                mets = plyr.metrics.bases_created
##                self.assertEqual(len(evts), len(mets))
##                for idx in range(0, len(mets)):
##                    self.assertEqual(convert_to_realtime_r(rep,evts[idx].second), mets[idx].second)
##
##       
##    def test_bases_created_tracker_against_json_data(self):
##        """
##        1. Test that the number of bases created is equivalent to the json data
##        2. Test that the times the bases were created is equivalent to the json data
##        """
##        #reps = sc2reader.load_replays("test_replays")
##        
####       rep_stats = None
####        with open("test_replays\\replay_info.json", "r") as fl:
####            rep_stats = json.load(fl)
####        
####        if rep_stats is None:
####           self.fail("could not open replay_info json file.")
####            
####        for rs in rep_stats:
####            replay = sc2reader.load_replay("test_replays\\"+rs['replay'])
####            
####            for bs in rs['bases']:
####                for idx in range(0, len(bs['players'])):
####                    met = replay.players[idx].metrics
####                    bc = bs['players'][idx]['bases_created']
####                    self.assertEqual(len(met.bases_created), len(bc))
####                    for bdx in range(0, len(bc)):
####                        self.assertEqual(met.bases_created[bdx].second, bc[bdx])
##        pass
##                        
##     
##    def test_supply_created_tracker_against_sc2reader(self):
##        #: TODO
##        reps = sc2reader.load_replays(REPLAY_DIR)
##        for rep in reps:
##            for plyr in rep.players:
##                ube = list(filter(lambda x: x.name == 'UnitBornEvent' and
##                                            (x.unit.is_worker or x.unit.is_army) and not
##                                            x.unit.hallucinated and
##                                            x.unit.owner.pid == plyr.pid, rep.events))
##                uie = list(filter(lambda x: x.name == 'UnitInitEvent' and 
##                                            (x.unit.is_worker or x.unit.is_army) and not 
##                                            x.unit.hallucinated and
##                                            x.unit.name == 'Archon' and
##                                            x.unit.owner.pid == plyr.pid, rep.events))
##                
##                evts = sorted(ube+uie, key=lambda x: x.second)
##                mets = plyr.metrics.supply_created
##                self.assertEqual(len(evts), len(mets))
##                for idx in range(0, len(mets)):
##                    self.assertEqual(convert_to_realtime_r(rep,evets[idx].second), mets[idx].second)
##        
##        
##    def test_supply_created_tracker_against_json_data(self):
##        #: TODO
##        pass
##        
##        
##    def test_apm_tracker_against_sc2reader(self):
##        #: TODO
##        pass
##        
##        
##    def test_apm_tracker_against_json_data(self):
##        #: TODO
##        pass
##        
##        
##    def test_supply_tracker_against_sc2reader(self):
##        #: TODO
##        pass
##        
##        
##    def test_supply_tracker_against_json_data(self):
##        #: TODO
##        pass
            
        
if __name__ == '__main__':
    unittest.main()
