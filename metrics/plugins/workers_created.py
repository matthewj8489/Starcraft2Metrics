import sc2metric
import metric_containers


class WorkersCreatedTracker(object):

    name = 'WorkersCreatedTracker'


    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()


    def handleUnitBornEvent(self,event,replay):
        if event.unit.is_worker:
            replay.player[event.unit.owner.pid].metrics.workers_created.append(
                Worker(event.second))
            
            
