from collections import defaultdict

from metrics.sc2metric import Sc2MetricAnalyzer
from metrics.util import convert_gametime_to_realtime_r


class APMTracker(object):
    """
    Provides ``player.metrics.avg_apm`` which is defined as the sum of 
    any Selection, ControlGroup, or Command event issued by the player 
    divided by the number of seconds played by the player (not
    necessarily the whole game) multiplied by 60.
    APM is 0 for games under 1 minute in length.
    """
    name = 'APMTracker'

    def __init__(self):
        #self._aps = {}
        self._actions = defaultdict(int)
        self._seconds_played = defaultdict(int)

    def handleInitGame(self, event, replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()
            self._actions[player.pid] = 0
            self._seconds_played[player.pid] = 0

    def handleControlGroupEvent(self, event, replay):
        self._actions[event.player.pid] += 1

    def handleSelectionEvent(self, event, replay):
        self._actions[event.player.pid] += 1
        
    def handleCommandEvent(self, event, replay):
        self._actions[event.player.pid] += 1

    def handlePlayerLeaveEvent(self, event, replay):
        self._seconds_played[event.player.pid] = convert_gametime_to_realtime_r(replay, event.second)

    def handleEndGame(self, event, replay):
        for player in replay.players:
            if self._actions[player.pid] > 0:
                player.metrics.avg_apm = self._actions[player.pid] / self._seconds_played[player.pid] * 60
