import spawningtool.parser

#metricfactory.spawningtool
def generateBuildOrderElements(self, file_path, player_name):
    bo_rep = spawningtool.parser.parse_replay(file_path)
    boe = []
    build_num = 1

    for plyr in bo_rep['players']:
        if plyr['name'] == player_name:
            for bo in plyr['buildOrder']:
                boe.append(BuildOrderElement(build_num,
                                             bo['name'],
                                             bo['supply'],
                                             bo['time'],
                                             bo['frame']))
                build_num += 1

    return boe


def generateSupplyCountArray(self):
    return None


def generateUnitListArray(self):
    # create an array whose elements are the units created at any given point
    # ['time':0, 'Probe':12, 'Zealot':0, ...]
        
