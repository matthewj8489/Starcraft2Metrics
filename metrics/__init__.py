
__version__ = "0.1.0"

import sc2reader

from metrics import plugins


sc2reader.engine.register_plugin(plugins.TimeConverter())
sc2reader.engine.register_plugin(plugins.SupplyTracker())
sc2reader.engine.register_plugin(plugins.BasesCreatedTracker())
sc2reader.engine.register_plugin(plugins.SupplyCreatedTracker())
sc2reader.engine.register_plugin(plugins.ResourceTracker())
sc2reader.engine.register_plugin(plugins.APMTracker())
sc2reader.engine.register_plugin(plugins.SPMTracker())
