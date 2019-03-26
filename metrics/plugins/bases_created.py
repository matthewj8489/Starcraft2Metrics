from sc2metric import Sc2MetricAnalyzer
from metric_containers import BaseCount
from util import convert_gametime_to_realtime_r

class BasesCreatedTracker(object):

    name = 'BasesCreatedTracker'


    def __init__(self):
        self._base_names = [
            'Nexus',
            'CommandCenter',
            'Hatchery'
            ]


    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()


    def handleUnitBornEvent(self,event,replay):
        if event.unit.is_building and (event.unit.name in self._base_names):
            replay.player[event.unit.owner.pid].metrics.bases_created.append(
                BaseCount(convert_gametime_to_realtime_r(replay, event.second)))


    def handleUnitDoneEvent(self,event,replay):
        if event.unit.is_building and (event.unit.name in self._base_names):
            replay.player[event.unit.owner.pid].metrics.bases_created.append(
                BaseCount(convert_gametime_to_realtime_r(replay, event.second)))
