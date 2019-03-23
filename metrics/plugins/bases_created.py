from sc2metric import Sc2MetricAnalyzer
from metric_containers import Base


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


    def handleUnitDoneEvent(self,event,replay):
        if event.unit.is_building and (event.unit.name in self._base_names):
            replay.player[event.unit.owner.pid].metrics.bases_created.append(
                Base(event.second))
