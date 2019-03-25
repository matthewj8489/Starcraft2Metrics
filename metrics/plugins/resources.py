from sc2metric import Sc2MetricAnalyzer
from metric_containers import ResourceCount


class ResourceTracker(object):

    name = 'ResourceTracker'

    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()


    def handlePlayerStatsEvent(self,event,replay):
        replay.player[event.pid].metrics.resources.append(
            ResourceCount(event.second,
                          (event.minerals_collection_rate + event.vespene_collection_rate),
                          (event.minerals_current + event.vespene_current)))
        
