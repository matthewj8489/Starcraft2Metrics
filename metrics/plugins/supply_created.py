from collections import defaultdict

from metrics.sc2metric import Sc2MetricAnalyzer
from metrics.metric_containers import SupplyCount
from metrics import util

class SupplyCreatedTracker(object):
    """
    Builds ``player.metrics.army_created``, ``player.metrics.workers_created``, and 
    ``player.metrics.supply_created`` arrays made of :class:`~metrics.metric_containers.SupplyCount`.
    The ``metrics`` being of the type :class:`~metrics.sc2metric.Sc2MetricAnalyzer`. The supplies
    are tracked whenever a unit is created. The unit's supply and a cumulative supply count of the
    army, workers, and total supply are tracked for the corresponding second.
    """

    name = 'SupplyCreatedTracker'


    def __init__(self):
        self._supply_created = defaultdict(int)
        self._workers_created = defaultdict(int)
        self._army_created = defaultdict(int)


    def _add_to_workers(self,event,replay):
        self._workers_created[event.unit.owner.pid] += event.unit.supply
        supp = SupplyCount(util.convert_gametime_to_realtime_r(replay,event.second),
                           self._workers_created[event.unit.owner.pid],
                           event.unit.supply,
                           event.unit.is_worker)
        replay.player[event.unit.owner.pid].metrics.workers_created.append(supp)
        
        
    def _add_to_army(self,event,replay):
        self._army_created[event.unit.owner.pid] += event.unit.supply
        supp = SupplyCount(util.convert_gametime_to_realtime_r(replay,event.second),
                           self._army_created[event.unit.owner.pid],
                           event.unit.supply,
                           event.unit.is_worker)
        replay.player[event.unit.owner.pid].metrics.army_created.append(supp)
        
        
    def _add_to_supply(self,event,replay):
        self._supply_created[event.unit.owner.pid] += event.unit.supply
        supp = SupplyCount(util.convert_gametime_to_realtime_r(replay,event.second),
                           self._supply_created[event.unit.owner.pid],
                           event.unit.supply,
                           event.unit.is_worker)
        replay.player[event.unit.owner.pid].metrics.supply_created.append(supp)


    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()
            self._supply_created[player.pid] = 0
            self._workers_created[player.pid] = 0
            self._army_created[player.pid] = 0


    def handleUnitBornEvent(self,event,replay):
        if event.unit.is_worker:
            self._add_to_supply(event,replay)
            self._add_to_workers(event,replay)
        elif (event.unit.is_army
              and not util.is_hallucinated(event.unit)
              and event.unit.name != "Archon"):
            self._add_to_supply(event,replay)
            self._add_to_army(event,replay)
            

    def handleUnitInitEvent(self,event,replay):
        if (event.unit.is_army and not util.is_hallucinated(event.unit) and event.unit.name != "Archon"):
            self._add_to_supply(event,replay)
            self._add_to_army(event,replay)
