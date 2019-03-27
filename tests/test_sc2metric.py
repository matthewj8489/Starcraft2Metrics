import sys

if __name__ == '__main__':
    sys.path.insert(0,"..\\")
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


import metrics
import sc2reader

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
        

##    def test_time_to_bases(self):
##        replay = sc2reader.load_replay("")
##        p1_met = replay.player[1].metrics
##
##        self.assertEqual(p1_met.time_to_bases_created(3), ?)
##        self.assertEqual(p1_met.time_to_bases_created(4), ?)
                         

if __name__ == '__main__':
    unittest.main()
