from metrics.sc2metric import Sc2MetricAnalyzer
from metrics.metric_containers import ResourceCount
from metrics.util import convert_gametime_to_realtime_r

class ResourceTracker(object):
    """
    Builds ``player.metrics.resources`` array made of :class:`~metrics.metric_containers.ResourceCount`.
    The ``metrics`` being of the type :class:`~metrics.sc2metric.Sc2MetricAnalyzer`. The resources
    tracked are the unspent resources (minerals + vespene) and the resource collection rate 
    (minerals + vespene).
    """
    
    name = 'ResourceTracker'

    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()


    def handlePlayerStatsEvent(self,event,replay):
        replay.player[event.pid].metrics.resources.append(
            ResourceCount(convert_gametime_to_realtime_r(replay,event.second),
                          (event.minerals_collection_rate + event.vespene_collection_rate),
                          (event.minerals_current + event.vespene_current)))
        
