from collections import defaultdict

from sc2metric import Sc2MetricAnalyzer
from metric_containers import SupplyCount
import util

class SupplyCreatedTracker(object):

    name = 'SupplyCreatedTracker'


    def __init__(self):
        self._supply_created = defaultdict(int)


    def _add_to_supply(self,event,replay):
        self._supply_created[event.unit.owner.pid] += event.unit.supply
        replay.player[event.unit.owner.pid].metrics.supply_created.append(
            SupplyCount(event.second, self._supply_created[event.unit.owner.pid], event.unit.supply, event.unit.is_worker))


    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()
            self._supply_created[player.pid] = 0


    def handleUnitBornEvent(self,event,replay):
        if event.unit.is_worker or (event.unit.is_army and not util.is_hallucinated(event.unit) and event.unit.name != "Archon"):
            self._add_to_supply(event,replay)


    def handleUnitInitEvent(self,event,replay):
        if (event.unit.is_army and not util.is_hallucinated(event.unit) and event.unit.name != "Archon"):
            self._add_to_supply(event,replay)
