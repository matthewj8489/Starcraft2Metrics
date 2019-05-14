import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import metrics
from metrics.sc2metric import Sc2MetricAnalyzer
from metrics.metric_containers import *

class TestSc2MetricAnalyzer(unittest.TestCase):

##    def setUp(self):
##        self.metrics = Sc2MetricAnalyzer()
##    
##    def tearDown(self):
##        self.metrics = None
        
    def test_first_max(self):
        met = Sc2MetricAnalyzer()
        met.supply.append(FoodCount(0, 15, 15)) # 0 second initial supply
        met.supply.append(FoodCount(50, 60, 101)) # nothing special
        met.supply.append(FoodCount(100, 197, 197)) #near max and near max supply made
        met.supply.append(FoodCount(130, 197, 200)) #near max
        met.supply.append(FoodCount(140, 198, 200)) #near max
        met.supply.append(FoodCount(150, 199, 200)) #near max
        met.supply.append(FoodCount(180, 200, 200)) #first max
        met.supply.append(FoodCount(200, 189, 200)) #dipped below max
        met.supply.append(FoodCount(220, 200, 200)) #got to max again
        
        self.assertEqual(met.first_max(), 180)
        
        
    def test_avg_sq(self):
        met = Sc2MetricAnalyzer()
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
        # SQ(i,u)=35(0.00137i-ln(u))+240
        # i = avg rcr = 783.3
        # u = aur = 223.3
        self.assertEqual(round(met.avg_sq(), 1), 88.3)
        
        
    def test_avg_sq_at_time(self):
        met = Sc2MetricAnalyzer()
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
        
        self.assertEqual(met.avg_sq_at_time(5), 0) # time before any input
        self.assertEqual(round(met.avg_sq_at_time(50), 1), 88.3) # at a time later than last recorded
        self.assertEqual(round(met.avg_sq_at_time(30), 1), 82.8) # in between 2 times
        
        
    def test_avg_sq_pre_max(self):
        met = Sc2MetricAnalyzer()
        met.supply.append(FoodCount(0, 15, 15)) # 0 second initial supply
        met.supply.append(FoodCount(50, 60, 101)) # nothing special
        met.supply.append(FoodCount(100, 197, 197)) #near max and near max supply made
        met.supply.append(FoodCount(130, 197, 200)) #near max
        met.supply.append(FoodCount(140, 198, 200)) #near max
        met.supply.append(FoodCount(150, 199, 200)) #near max
        met.supply.append(FoodCount(180, 200, 200)) #first max
        met.supply.append(FoodCount(200, 189, 200)) #dipped below max
        met.supply.append(FoodCount(220, 200, 200)) #got to max again
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
        met.resources.append(ResourceCount(180, 3100, 850))
        met.resources.append(ResourceCount(200, 3300, 1050))
        met.resources.append(ResourceCount(220, 3000, 950))
        
        self.assertEqual(round(met.avg_sq_pre_max(), 1), 97.4)
        
        
    def test_avg_sq_pre_max_when_never_maxed(self):
        met = Sc2MetricAnalyzer()
        met.supply.append(FoodCount(0, 15, 15)) # 0 second initial supply
        met.supply.append(FoodCount(50, 60, 101)) # nothing special
        met.supply.append(FoodCount(100, 197, 197)) #near max and near max supply made
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
        
        self.assertEqual(round(met.avg_sq_pre_max(), 1), 88.3)     
        
        
    def test_aur(self):
        met = Sc2MetricAnalyzer()
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
        
        # shouldn't avg rcr care about the time (second) that this value was read when calculating average?
        self.assertEqual(round(met.aur(), 1), 223.3)
        
        
    def test_aur_at_time(self):
        met = Sc2MetricAnalyzer()
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
        
        self.assertIsNone(met.aur_at_time(5)) # bad input
        self.assertEqual(round(met.aur_at_time(50), 1), 223.3) # at a time later than last recorded
        self.assertEqual(round(met.aur_at_time(30), 1), 210.0) # in between 2 times
        
        
    def test_aur_pre_max(self):
        met = Sc2MetricAnalyzer()
        met.supply.append(FoodCount(0, 15, 15)) # 0 second initial supply
        met.supply.append(FoodCount(50, 60, 101)) # nothing special
        met.supply.append(FoodCount(100, 197, 197)) #near max and near max supply made
        met.supply.append(FoodCount(130, 197, 200)) #near max
        met.supply.append(FoodCount(140, 198, 200)) #near max
        met.supply.append(FoodCount(150, 199, 200)) #near max
        met.supply.append(FoodCount(180, 200, 200)) #first max
        met.supply.append(FoodCount(200, 189, 200)) #dipped below max
        met.supply.append(FoodCount(220, 200, 200)) #got to max again
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
        met.resources.append(ResourceCount(180, 3100, 850))
        met.resources.append(ResourceCount(200, 3300, 1050))
        met.resources.append(ResourceCount(220, 3000, 950))
        
        self.assertEqual(round(met.aur_pre_max(), 1), 380)
        
        
    def test_aur_pre_max_when_never_maxed(self):
        met = Sc2MetricAnalyzer()
        met.supply.append(FoodCount(0, 15, 15)) # 0 second initial supply
        met.supply.append(FoodCount(50, 60, 101)) # nothing special
        met.supply.append(FoodCount(100, 197, 197)) #near max and near max supply made
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
        
        self.assertEqual(round(met.aur_pre_max(), 1), 223.3)
        
        
    def test_avg_rcr(self):
        met = Sc2MetricAnalyzer()
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
    
        # shouldn't avg rcr care about the time (second) that this value was read when calculating average?    
        self.assertEqual(round(met.avg_rcr(), 1), 783.3)
        
        
    def test_avg_rcr_at_time(self):
        met = Sc2MetricAnalyzer()
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
    
        self.assertIsNone(met.avg_rcr_at_time(5)) # bad input
        self.assertEqual(round(met.avg_rcr_at_time(50), 1), 783.3) # at a time later than last recorded
        self.assertEqual(round(met.avg_rcr_at_time(30), 1), 625.0) # in between 2 times
        
    
    def test_avg_rcr_pre_max(self):
        met = Sc2MetricAnalyzer()
        met.supply.append(FoodCount(0, 15, 15)) # 0 second initial supply
        met.supply.append(FoodCount(50, 60, 101)) # nothing special
        met.supply.append(FoodCount(100, 197, 197)) #near max and near max supply made
        met.supply.append(FoodCount(130, 197, 200)) #near max
        met.supply.append(FoodCount(140, 198, 200)) #near max
        met.supply.append(FoodCount(150, 199, 200)) #near max
        met.supply.append(FoodCount(180, 200, 200)) #first max
        met.supply.append(FoodCount(200, 189, 200)) #dipped below max
        met.supply.append(FoodCount(220, 200, 200)) #got to max again
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
        met.resources.append(ResourceCount(180, 3100, 850))
        met.resources.append(ResourceCount(200, 3300, 1050))
        met.resources.append(ResourceCount(220, 3000, 950))
        
        self.assertEqual(round(met.avg_rcr_pre_max(), 1), 1362.5)    
        
        
    def test_avg_rcr_pre_max_when_never_maxed(self):
        met = Sc2MetricAnalyzer()
        met.supply.append(FoodCount(0, 15, 15)) # 0 second initial supply
        met.supply.append(FoodCount(50, 60, 101)) # nothing special
        met.supply.append(FoodCount(100, 197, 197)) #near max and near max supply made
        met.resources.append(ResourceCount(10, 500, 120))
        met.resources.append(ResourceCount(20, 750, 300))
        met.resources.append(ResourceCount(40, 1100, 250))
        
        self.assertEqual(round(met.avg_rcr_pre_max(), 1), 783.3)
        
    
    def test_supply_capped(self):
        met = Sc2MetricAnalyzer()
        met.supply.append(FoodCount(0, 12, 15))
        met.supply.append(FoodCount(5, 14, 15)) # no supply block
        
        self.assertEqual(met.supply_capped(), 0)
        
        met.supply.append(FoodCount(30, 15, 15)) # supply cap begins
        met.supply.append(FoodCount(50, 15, 22)) # supply cap resolved by gaining supply buildings
        
        self.assertEqual(met.supply_capped(), 20)
        
        met.supply.append(FoodCount(60, 22, 22)) # supply cap begins
        met.supply.append(FoodCount(65, 20, 22)) # supply cap resolved by losing supply
        
        self.assertEqual(met.supply_capped(), 25)
        
        met.supply.append(FoodCount(73, 20, 15)) # supply cap from losing supply building
        met.supply.append(FoodCount(80, 20, 22)) # supply cap resolved
        
        self.assertEqual(met.supply_capped(), 32)
        
        met.supply.append(FoodCount(160, 198, 192)) # supply cap begins
        met.supply.append(FoodCount(161, 198, 200)) # supply resolved by reaching 200 supply buildings made
        
        self.assertEqual(met.supply_capped(), 33)
        
        
    def test_first_time_to_supply(self):
        met = Sc2MetricAnalyzer()
        
        met.supply.append(FoodCount(0, 10, 15))
        met.supply.append(FoodCount(20, 25, 30))
        
        self.assertEqual(met.first_time_to_supply(0), 0) # less than the first supply
        self.assertEqual(met.first_time_to_supply(20), 20) # in between supplies
        self.assertEqual(met.first_time_to_supply(25), 20) # exact
        self.assertEqual(met.first_time_to_supply(26), -1) # more than total supply tracked
        
        
    def test_time_to_supply(self):
        met = Sc2MetricAnalyzer()
        
        met.supply.append(FoodCount(5, 10, 15))
        met.supply.append(FoodCount(20, 25, 30))
        
        self.assertEqual(met.supply_at_time(0), 0) # less than the first supply
        self.assertEqual(met.supply_at_time(10), 10) # in between
        self.assertEqual(met.supply_at_time(20), 25) # exact
        self.assertEqual(met.supply_at_time(21), 25) # past the last time
    
        
    def test_workers_created_at_time(self):
        met = Sc2MetricAnalyzer()
        
        self.assertEqual(met.workers_created_at_time(5), 0) # no workers created
        
        met.workers_created.append(SupplyCount(1, 1, 1, True))
        met.workers_created.append(SupplyCount(20, 8, 1, True))
        met.workers_created.append(SupplyCount(25, 9, 1, True))
        
        self.assertEqual(met.workers_created_at_time(0), 0) # before anything tracked
        self.assertEqual(met.workers_created_at_time(20), 2) # exact time
        self.assertEqual(met.workers_created_at_time(15), 1) # in between case
        self.assertEqual(met.workers_created_at_time(30), 3) # longer than last tracked supply time
        
        
    def test_army_created_at_time(self):
        met = Sc2MetricAnalyzer()
        
        self.assertEqual(met.army_created_at_time(5), 0) # no army created
        
        met.army_created.append(SupplyCount(10, 30, 6, False))
        met.army_created.append(SupplyCount(25, 44, 2, False))
        met.army_created.append(SupplyCount(30, 48, 4, False))
        
        self.assertEqual(met.army_created_at_time(5), 0) # before anything tracked
        self.assertEqual(met.army_created_at_time(25), 44) # exact time
        self.assertEqual(met.army_created_at_time(20), 30) # in between case
        self.assertEqual(met.army_created_at_time(40), 48) # longer than last tracked supply time        
        
        
    def test_supply_created_at_time(self):
        met = Sc2MetricAnalyzer()
        met.supply_created.append(SupplyCount(0, 1, 1, True)) # worker supply
        met.supply_created.append(SupplyCount(0, 2, 1, True)) # two worker supplies tracked at zero seconds
        met.supply_created.append(SupplyCount(20, 4, 2, False)) # army supply
        met.supply_created.append(SupplyCount(50, 8, 4, False)) 
        met.supply_created.append(SupplyCount(55, 9, 1, True))
        met.supply_created.append(SupplyCount(60, 11, 2, False))
        met.supply_created.append(SupplyCount(60, 11, 2, False)) # two army supplies tracked at zero seconds
        
        self.assertEqual(met.supply_created_at_time(0), 2) # 0 seconds
        self.assertEqual(met.supply_created_at_time(55), 9) # exact time
        self.assertEqual(met.supply_created_at_time(57), 9) # in between 2 times
        self.assertEqual(met.supply_created_at_time(70), 11) # greater than greatest time 
        
        
    def test_supply_created_at_time_when_no_supply_created_tracked(self):
        met = Sc2MetricAnalyzer()
        
        self.assertEqual(met.supply_created_at_time(0), 0)
        
        
    def test_supply_created_at_time_when_first_supply_created_occurred_after_supplied_time(self):
        met = Sc2MetricAnalyzer()
        met.supply_created.append(SupplyCount(1, 1, 1, True)) # worker supply
        
        self.assertEqual(met.supply_created_at_time(0), 0)
        
        
    def test_time_to_workers_created(self):
        met = Sc2MetricAnalyzer()
        met.workers_created.append(SupplyCount(0, 1, 1, True))
        met.workers_created.append(SupplyCount(20, 8, 1, True))
        met.workers_created.append(SupplyCount(25, 9, 1, True))
                
        self.assertIsNone(met.time_to_workers_created(0)) # bad input case
        self.assertIsNone(met.time_to_workers_created(6)) # bad input case
        self.assertEqual(met.time_to_workers_created(1), 0)
        self.assertEqual(met.time_to_workers_created(2), 20)
        self.assertEqual(met.time_to_workers_created(3), 25)
        
                
    def test_time_to_supply_created(self):
        met = Sc2MetricAnalyzer()
        met.supply_created.append(SupplyCount(0, 1, 1, True)) # worker supply
        met.supply_created.append(SupplyCount(0, 2, 1, True)) # two worker supplies tracked at zero seconds
        met.supply_created.append(SupplyCount(20, 4, 2, False)) # army supply
        met.supply_created.append(SupplyCount(50, 8, 4, False)) 
        met.supply_created.append(SupplyCount(55, 9, 1, True))
        met.supply_created.append(SupplyCount(60, 11, 2, False))
        met.supply_created.append(SupplyCount(60, 11, 2, False)) # two army supplies tracked at zero seconds
        
        self.assertIsNone(met.time_to_supply_created(0)) # bad input case
        self.assertEqual(met.time_to_supply_created(8), 50) # exact supply
        self.assertEqual(met.time_to_supply_created(10), 60) # in between 2 supplies tracked
        self.assertEqual(met.time_to_supply_created(20), 60) # more supply than what was tracked
        
        
    def test_time_to_supply_created_max_workers(self):
        met = Sc2MetricAnalyzer()
        met.supply_created.append(SupplyCount(0, 1, 1, True)) # worker supply
        met.supply_created.append(SupplyCount(0, 2, 1, True)) # two worker supplies tracked at zero seconds
        met.supply_created.append(SupplyCount(20, 4, 2, False)) # army supply
        met.supply_created.append(SupplyCount(50, 8, 4, False)) 
        met.supply_created.append(SupplyCount(55, 9, 1, True))
        met.supply_created.append(SupplyCount(60, 11, 2, False))
        met.supply_created.append(SupplyCount(60, 11, 2, False)) # two army supplies tracked at zero seconds
        
        # bad inputs
        self.assertIsNone(met.time_to_supply_created_max_workers(0, 1))
        
        # max workers > total workers tracked
        self.assertEqual(met.time_to_supply_created_max_workers(8, 10), 50) # exact supply
        self.assertEqual(met.time_to_supply_created_max_workers(10, 10), 60) # in between 2 supplies
        self.assertEqual(met.time_to_supply_created_max_workers(20, 10), 60) # more supply than what was tracked
        
        # max workers < total workers tracked
        self.assertEqual(met.time_to_supply_created_max_workers(7, 1), 50) # exact supply
        self.assertEqual(met.time_to_supply_created_max_workers(8, 1), 60) 
        self.assertIsNone(met.time_to_supply_created_max_workers(20, 2)) # more supply than what was tracked
        
    
    def test_time_to_bases_created(self):
        met = Sc2MetricAnalyzer()
        met.bases_created.append(BaseCount(0))
        met.bases_created.append(BaseCount(45))
        met.bases_created.append(BaseCount(80))
        
        self.assertIsNone(met.time_to_bases_created(0)) # bad input case
        self.assertIsNone(met.time_to_bases_created(4)) # bad input case
        self.assertEqual(met.time_to_bases_created(1), 0)
        self.assertEqual(met.time_to_bases_created(2), 45)
        self.assertEqual(met.time_to_bases_created(3), 80)
        
        
if __name__ == '__main__':
    unittest.main()
