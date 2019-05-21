from collections import defaultdict

from metrics.sc2metric import Sc2MetricAnalyzer
from metrics.util import convert_gametime_to_realtime_r


class SPMTracker(object):
    """
    Provides ``player.metrics.avg_spm`` which is defined as the sum of
    any Camera event issued by the player, divided by the number of 
    seconds played by the player (not necessarily the whole game)
    multiplied by 60. A Camera event is issued any time the camera is
    moved.
    SPM is 0 for games under 1 minute in length.
    """
    
    name = 'SPMTracker'
    
    def __init__(self):
        self._sps = {}
        self._seconds_played = defaultdict(int)
        self._location = {}
        
    def handleInitGame(self, event, replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()
            self._sps[player.pid] = defaultdict(int)
            self._location[player.pid] = (0, 0)
            
    def handleCameraEvent(self, event, replay):
        loc_diff = abs(event.location[0] - self._location[event.player.pid][0]) + abs(event.location[1] - self._location[event.player.pid][1])
        self._location[event.player.pid] = event.location
        if loc_diff > 15:
            self._sps[event.player.pid][convert_gametime_to_realtime_r(replay, event.second)] += 1
        
    def handlePlayerLeaveEvent(self, event, replay):
        self._seconds_played[event.player.pid] = convert_gametime_to_realtime_r(replay, event.second)
        
    def handleEndGame(self, event, replay):
        for player in replay.players:
            if len(self._sps[player.pid].keys()) > 0:
                player.metrics.avg_spm = sum(self._sps[player.pid].values())/self._seconds_played[player.pid]*60
            else:
                player.metrics.avg_spm = 0