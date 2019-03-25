os.environ['SC2READER_CACHE_DIR'] = "temp/cache"
os.environ['SC2READER_CACHE_MAX_SIZE'] = 100


import sc2reader


class Sc2TrendAnalyzer(object):

    # should we be taking in replay files and creating metric classes for each of them and traversing those metric classes?
    # what about the case of not parsing replays already in a metric raw data file?
    # in that case, should we instead be taking in a metric dictionary? and analyzing and deriving trends from that?

    def __init__(self, replay_files, player_name):
        self._replays = replay_files
        self._player_name = player_name

        


    def sq(self, 
