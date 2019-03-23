from sc2metric import Sc2MetricAnalyzer
from metric_containers import SupplyCount


class WorkersCreatedTracker(object):

    name = 'WorkersCreatedTracker'


    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()


    def handleUnitBornEvent(self,event,replay):
        if event.unit.is_worker:
            replay.player[event.unit.owner.pid].metrics.workers_created.append(
                SupplyCount(event.second,
                            len(replay.player[event.unit.owner.pid].metrics.workers_created)+1,
                            1,
                            False))
            
            
