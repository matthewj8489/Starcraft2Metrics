##import sc2reader
##from plugins.supply import SupplyTracker
##from plugins.bases_created import BasesCreatedTracker
##from plugins.supply_created import SupplyCreatedTracker
##from plugins.resources import ResourceTracker
##from plugins.apm import APMTracker
##
##sc2reader.engine.register_plugin(SupplyTracker())
##sc2reader.engine.register_plugin(BasesCreatedTracker())
##sc2reader.engine.register_plugin(SupplyCreatedTracker())
##sc2reader.engine.register_plugin(ResourceTracker())
##sc2reader.engine.register_plugin(APMTracker())

import sys
if __name__ == '__main__':
    sys.path.insert(0,"..\\")

import sc2reader

import metrics

replay = sc2reader.load_replay("..\\tests\\test_replays\\standard_1v1.SC2Replay")
p1_met = replay.player[1].metrics

import pickle

p1_met_pickled = pickle.dumps(p1_met)
p1_met_unp = pickle.loads(p1_met_pickled)

