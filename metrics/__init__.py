__version__ = "0.1.0"

import sc2reader

import util

from metrics import plugins


sc2reader.engine.register_plugin(SupplyTracker())
sc2reader.engine.register_plugin(BasesCreatedTracker())
sc2reader.engine.register_plugin(SupplyCreatedTracker())
sc2reader.engine.register_plugin(ResourceTracker())
sc2reader.engine.register_plugin(APMTracker())
