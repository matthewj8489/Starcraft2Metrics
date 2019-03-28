from collections import defaultdict

from metrics.sc2metric import Sc2MetricAnalyzer
from metrics.metric_containers import SupplyCount
from metrics import util

class SupplyCreatedTracker(object):

    name = 'SupplyCreatedTracker'


    def __init__(self):
        self._supply_created = defaultdict(int)


    def _add_to_supply(self,event,replay):
        self._supply_created[event.unit.owner.pid] += event.unit.supply
        supp = SupplyCount(util.convert_gametime_to_realtime_r(replay,event.second),
                           self._supply_created[event.unit.owner.pid],
                           event.unit.supply,
                           event.unit.is_worker)
        replay.player[event.unit.owner.pid].metrics.supply_created.append(supp)
        if event.unit.is_worker:
            replay.player[event.unit.owner.pid].metrics.workers_created.append(supp)
        elif event.unit.is_army:
            replay.player[event.unit.owner.pid].metrics.army_created.append(supp)


    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()
            self._supply_created[player.pid] = 0


    def handleUnitBornEvent(self,event,replay):
        if event.unit.is_worker or (event.unit.is_army
                                    and not util.is_hallucinated(event.unit)
                                    and event.unit.name != "Archon"):
            self._add_to_supply(event,replay)


    def handleUnitInitEvent(self,event,replay):
        if (event.unit.is_army and not util.is_hallucinated(event.unit) and event.unit.name != "Archon"):
            self._add_to_supply(event,replay)
