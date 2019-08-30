import sc2reader

from metrics.metric_containers import *
from metrics.util import convert_to_realtime_r

class Sc2ReaderFactory(object):

    def __init__(self, file_path):
        self._replay = sc2reader.load_replay(file_path)

    def generateResourcesTracked(self, player_name):
        res = []
        
        for plyr in self._replay.players:
            if plyr.name == player_name:
                plyr_stats_events = list(filter(lambda evts: evts.name == 'PlayerStatsEvent', plyr.events))
                for evt in plyr_stats_events:
                    res.append(ResourceCount(convert_to_realtime_r(self._replay, evt.second),
                                             (evt.minerals_collection_rate + evt.vespene_collection_rate),
                                             (evt.minerals_current + evt.vespene_current)))
                break

        return res
