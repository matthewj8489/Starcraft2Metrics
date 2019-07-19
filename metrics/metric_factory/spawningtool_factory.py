import spawningtool.parser
from metric_containers import *

#metricfactory.spawningtool
def generateBuildOrderElements(file_path, player_name):
    bo_rep = spawningtool.parser.parse_replay(file_path)
    boe = []
    build_num = 1

    for plyr in bo_rep['players'].values():
        if plyr['name'] == player_name:
            for bo in plyr['buildOrder']:
                boe.append(BuildOrderElement(build_num,
                                             bo['name'],
                                             bo['supply'],
                                             convertTimeStringToSeconds(bo['time']),
                                             bo['frame']))
                build_num += 1

    return boe


def convertTimeStringToSeconds(time_str):
    # 1:52 --> 112
    time_s = 0
    splts = time_str.split(':')

    time_s = int(splts[0]) * 60 + int(splts[1])

    return time_s


def generateSupplyCountArray():
    return None


def generateUnitListArray():
    # create an array whose elements are the units created at any given point
    # ['time':0, 'Probe':12, 'Zealot':0, ...]
    return None
        
