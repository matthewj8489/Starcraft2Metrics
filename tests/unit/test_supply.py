import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from unittest.mock import MagicMock

from metrics.sc2metric import Sc2MetricAnalyzer    
from metrics.plugins.supply import SupplyTracker


class TestSupplyTrackerPlugin(unittest.TestCase):

    def _generate_stub_replay(self):
        return MagicMock(players=[MagicMock(units=[]), MagicMock(units=[])],
                         game_length = MagicMock(seconds=100),
                         game_fps = 1,
                         frames = 100) # this will set everything up so that 1 game sec = 1 real sec)
        
               
    def _add_unit(self, player, second_created, second_died, supply):
        player.units.append(MagicMock(hallucinated=False,
                                      is_building=False,
                                      supply=supply,
                                      started_at=second_created,
                                      died_at=second_died,
                                      name=''))
        
        
    def _add_pylon(self, player, second_created, second_died, supply):
        player.units.append(MagicMock(hallucinated=False,
                                      is_building=True,
                                      supply=supply,
                                      started_at=second_created,
                                      died_at=second_died,
                                      name='Pylon'))

    def test_handleInitGame(self):
        rep = MagicMock(players=[MagicMock(), MagicMock()])
        sup = SupplyTracker()
        sup.handleInitGame(None, rep)
        for plyr in rep.players:
            self.assertTrue(hasattr(plyr, 'metrics'))
            self.assertIsNotNone(plyr.metrics)
            self.assertIs(type(plyr.metrics), Sc2MetricAnalyzer)
        
        
    def test_handleEndGame(self):
        rep = self._generate_stub_replay()
        sup = SupplyTracker()
        
        self._add_unit(rep.players[0], 1, 3, 1)
        self._add_pylon(rep.players[0], 1, 4, 8)
        
        sup.handleEndGame(None, rep)
        p1_met = rep.players[0].metrics
        
        for sp in p1_met.supply:
            print(sp.second, " ", sp.supply_used, "/", sp.supply_made)
        
        self.assertEqual(len(p1_met.supply), 3)
        self.assertEqual(p1_met.supply[0].supply_used, 1)
        self.assertEqual(p1_met.supply[0].supply_made, 8)
        self.assertEqual(p1_met.supply[0].second, 1)
        self.assertEqual(p1_met.supply[1].supply_used, 0)
        self.assertEqual(p1_met.supply[1].second, 3)
        self.assertEqual(p1_met.supply[2].supply_made, 0)
        self.assertEqual(p1_met.supply[2].second, 4)
        

        
if __name__ == '__main__':
    unittest.main()