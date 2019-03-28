import sys

if __name__ == '__main__':
    sys.path.insert(0,"..\\")
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import metrics
from metrics import plugins
import sc2reader


class Foo(object):
    pass


class TestSupplyCreatedTracked(unittest.TestCase):

##    def test_add_to_supply(self):
##
##        replay = sc2reader.load_replay("test_replays\\standard_1v1.SC2Replay")
##        sup_plg = None
##        for plg in sc2reader.engine.plugins():
##            if plg.name is metrics.plugins.SupplyCreatedTracker.name:
##                sup_plg = plg
##
##        if sup_plg == None:
##            self.fail("The Supply Created Tracker plugin is not being registered.")
##
##        #event = sc2reader.events.UnitBornEvent
##
##        ube = None
##        for evt in replay.events:
##            if evt.name is sc2reader.events.UnitBornEvent.name:
##                ube = evt
##                break


    def test_add_to_supply_with_dummy_data(self):

        # dummy event, replay
        evt = Foo()
        evt.unit = Foo()
        evt.unit.owner = Foo()
        evt.unit.owner.pid = 1
        evt.unit.supply = 4
        evt.unit.is_worker = False
        evt.unit.is_army = True
        evt.second = 50

        rep = sc2reader.load_replay("test_replays\\standard_1v1.SC2Replay")
        replay = Foo()
        replay.player = {1: Foo()}
        replay.player[1].metrics = Foo()
        replay.player[1].metrics.supply_created = []
        replay.player[1].metrics.workers_created = []
        replay.player[1].metrics.army_created = []
        replay.frames = rep.frames
        replay.game_fps = rep.game_fps
        replay.game_length = rep.game_length

        # test that army supply counting works
        trk = metrics.plugins.SupplyCreatedTracker()
        trk._add_to_supply(evt, replay)
        
        self.assertNotEqual(len(replay.player[1].metrics.supply_created), 0)
        self.assertNotEqual(len(replay.player[1].metrics.army_created), 0)

        # test that worker supply counting works
        evt.unit.supply = 1
        evt.unit.is_worker = True
        evt.unit.is_army = False
        evt.second = 30
        replay.player[1].metrics.supply_created = []
        replay.player[1].metrics.workers_created = []
        replay.player[1].metrics.army_created = []
        
        trk = metrics.plugins.SupplyCreatedTracker()
        trk._add_to_supply(evt, replay)
        
        self.assertNotEqual(len(replay.player[1].metrics.supply_created), 0)
        self.assertNotEqual(len(replay.player[1].metrics.workers_created), 0)
        

if __name__ == '__main__':
    unittest.main()
