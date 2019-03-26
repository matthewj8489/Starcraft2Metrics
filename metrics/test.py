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
    sys.path.insert(0,"C:\\Users\\matthew\\Documents\\gitprojects\\Starcraft2Metrics\\")

import sc2reader

import metrics

replay = sc2reader.load_replay("..\\test\\test_replays\\Year Zero LE (9).SC2Replay")
p1_met = replay.player[1].metrics
