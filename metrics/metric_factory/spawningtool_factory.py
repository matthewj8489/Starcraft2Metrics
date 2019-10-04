import os
import json
from datetime import datetime

import spawningtool.parser
from metrics.metric_containers import *

#metricfactory.spawningtool
class SpawningtoolFactory(object):

    def __init__(self, file_path, cache_dir=None):
        self._build = spawningtool.parser.parse_replay(file_path, cache_dir=cache_dir)
    
    def generateBuildOrderElements(self, player_name):
        boe = []
        build_num = 1

        for plyr in self._build['players'].values():
            if plyr['name'] == player_name:
                for bo in plyr['buildOrder']:
                    boe.append(BuildOrderElement(build_num,
                                                 bo['name'],
                                                 bo['supply'],
                                                 self._convertTimeStringToSeconds(bo['time']),
                                                 bo['frame']))
                    build_num += 1

        return boe


    def generateReplayMetadata(self):
        meta = ReplayMetadata()

        meta.game_length = self._build['frames'] / self._build['frames_per_second']
        meta.date = datetime.utcfromtimestamp(self._build['unix_timestamp']).strftime('%Y-%m-%d %H:%M;%S')
        for plyr in self._build['players'].values():
            meta.players.append("({0}){1}".format(plyr['race'][0], plyr['name']))
            meta.player.append(plyr)
            if plyr['is_winner']:
                meta.winner = plyr['name']

        return meta
        

    def generateSupplyCountArray(self):
        return None


    def generateUnitListArray(self):
        # create an array whose elements are the units created at any given point
        # ['time':0, 'Probe':12, 'Zealot':0, ...]
        return None


    def _convertTimeStringToSeconds(self, time_str):
        # 1:52 --> 112
        time_s = 0
        splts = time_str.split(':')

        time_s = int(splts[0]) * 60 + int(splts[1])

        return time_s
        
