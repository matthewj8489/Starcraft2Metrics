import sc2reader
from plugins.supply import SupplyTracker
#from plugins.workers_created import WorkersCreatedTracker
#from plugins.army_created import ArmyCreatedTracker
from plugins.bases_created import BasesCreatedTracker
from plugins.supply_created import SupplyCreatedTracker
from plugins.resources import ResourceTracker

sc2reader.engine.register_plugin(SupplyTracker())
#sc2reader.engine.register_plugin(WorkersCreatedTracker())
#sc2reader.engine.register_plugin(ArmyCreatedTracker())
sc2reader.engine.register_plugin(BasesCreatedTracker())
sc2reader.engine.register_plugin(SupplyCreatedTracker())
sc2reader.engine.register_plugin(ResourceTracker())

replay = sc2reader.load_replay("..\\test\\test_replays\\Year Zero LE (9).SC2Replay")
p1_met = replay.player[1].metrics
