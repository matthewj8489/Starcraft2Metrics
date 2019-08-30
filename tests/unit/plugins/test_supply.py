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
        
        
    def _add_worker(self, player, second_created, second_died):
        mock = MagicMock(hallucinated=False,
                         is_building=False,
                         is_worker=True,
                         is_army=False,
                         supply=1,
                         started_at=second_created,
                         died_at=second_died)
        mock.name = ''
        player.units.append(mock)
        
        
    def _add_army(self, player, second_created, second_died, supply, halluc):
        mock = MagicMock(hallucinated=halluc,
                         is_building=False,
                         is_worker=False,
                         is_army=True,
                         supply=supply,
                         started_at=second_created,
                         died_at=second_died)
        mock.name = ''
        player.units.append(mock)
        
        
    def _add_pylon(self, player, second_created, second_died):
        # mock.name must be setup in this way due to the nature of MagicMock
        # see here: https://docs.python.org/3/library/unittest.mock.html#mock-names-and-the-name-attribute
        mock = MagicMock(hallucinated=False,
                                      is_building=True,
                                      is_worker=False,
                                      is_army=False,
                                      supply=0,
                                      started_at=second_created,
                                      died_at=second_died)
        mock.name = 'Pylon'
        player.units.append(mock)

        
    def _add_nexus(self, player, second_created, second_died):
        mock = MagicMock(hallucinated=False,
                                      is_building=True,
                                      is_worker=False,
                                      is_army=False,
                                      supply=0,
                                      started_at=second_created,
                                      died_at=second_died)
        mock.name = 'Nexus'
        player.units.append(mock)
        
        
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
        
        self._add_worker(rep.players[0], 1, 3)
        self._add_pylon(rep.players[0], 1, 4)
        
        sup.handleEndGame(None, rep)
        p1_met = rep.players[0].metrics
                
        self.assertEqual(len(p1_met.supply), 3)
        self.assertEqual(p1_met.supply[0].supply_used, 1)
        self.assertEqual(p1_met.supply[0].supply_made, 8)
        self.assertEqual(p1_met.supply[0].second, 1)
        self.assertEqual(p1_met.supply[1].supply_used, 0)
        self.assertEqual(p1_met.supply[1].second, 3)
        self.assertEqual(p1_met.supply[2].supply_made, 0)
        self.assertEqual(p1_met.supply[2].second, 4)
        

    def test_handleEndGame_when_hallucinated_units_present(self):
        rep = self._generate_stub_replay()
        sup = SupplyTracker()
        
        self._add_army(rep.players[0], 3, 8, 4, True)
        
        sup.handleEndGame(None, rep)
        p1_met = rep.players[0].metrics
        
        self.assertEqual(len(p1_met.supply), 0)
        
        
    def test_handleEndGame_when_nexus_created(self):
        rep = self._generate_stub_replay()
        sup = SupplyTracker()
        
        self._add_nexus(rep.players[0], 1, None)
        
        sup.handleEndGame(None, rep)
        p1_met = rep.players[0].metrics
        
        self.assertEqual(len(p1_met.supply), 1)
        self.assertEqual(p1_met.supply[0].supply_made, 15)
    
    
    def test_handleEndGame_when_unit_never_died(self):
        rep = self._generate_stub_replay()
        sup = SupplyTracker()
        
        self._add_nexus(rep.players[0], 1, None)
        self._add_army(rep.players[0], 5, None, 8, False)
        
        sup.handleEndGame(None, rep)
        p1_met = rep.players[0].metrics
        
        self.assertEqual(len(p1_met.supply), 2)
        self.assertEqual(p1_met.supply[0].supply_made, 15)
        self.assertEqual(p1_met.supply[1].supply_made, 15)
        self.assertEqual(p1_met.supply[1].supply_used, 8)
        
        
if __name__ == '__main__':
    unittest.main()