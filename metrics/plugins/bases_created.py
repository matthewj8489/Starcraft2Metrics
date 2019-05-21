from metrics.sc2metric import Sc2MetricAnalyzer
from metrics.metric_containers import BaseCount
from metrics.util import convert_to_realtime_r

class BasesCreatedTracker(object):
    """
    Builds ``player.metrics.bases_created`` array made of :class:`~metrics.metric_containers.BaseCount`.
    The ``metrics`` being of the type :class:`~metrics.sc2metric.Sc2MetricAnalyzer`. The bases are
    tracked every time a *Nexus*, *CommandCenter*, or *Hatchery* is completed.
    """

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
                BaseCount(convert_to_realtime_r(replay, event.second)))


    def handleUnitDoneEvent(self,event,replay):
        if event.unit.is_building and (event.unit.name in self._base_names):
            replay.player[event.unit.owner.pid].metrics.bases_created.append(
                BaseCount(convert_to_realtime_r(replay, event.second)))
