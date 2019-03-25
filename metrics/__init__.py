import util

import sc2reader
from plugins.supply import SupplyTracker
from plugins.bases_created import BasesCreatedTracker
from plugins.supply_created import SupplyCreatedTracker
from plugins.resources import ResourceTracker

sc2reader.engine.register_plugin(SupplyTracker())
sc2reader.engine.register_plugin(BasesCreatedTracker())
sc2reader.engine.register_plugin(SupplyCreatedTracker())
sc2reader.engine.register_plugin(ResourceTracker())
