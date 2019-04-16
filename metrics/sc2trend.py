import statistics

from sc2metric import Sc2MetricAnalyzer


class Sc2TrendAnalyzer(object):

    # should we be taking in replay files and creating metric classes for each of them and traversing those metric classes?
    # what about the case of not parsing replays already in a metric raw data file?
    # in that case, should we instead be taking in a metric dictionary? and analyzing and deriving trends from that?

    def __init__(self, replay_files, player_name):
        self._replays = replay_files
        self._player_name = player_name

        
    def __init__(self, metric):
        self._metrics = metric
        #self.best = TrendData(metric)
        


    # best()
    # best(start_date, end_date)
    # best_weekly()
    # best_monthly()
    # avg()
    # avg(start_date, end_date)
    # avg_weekly()
    # avg_monthly()
    # std_dev()
    # std_dev(start_date, end_date)
    # std_dev_weekly()
    # std_dev_monthly()

    # specific time period

##    class TrendData(object):
##
##        def __init__(self, data):
##            self._data = data
##
##        def get_value():
##
##        def get_value(start_date, end_data):
##
##        def value_per_week():
##
##        def value_per_month():

    def best(self):
        return max(self._metrics)

    def avg(self):
        return statistics.mean(self._metrics)

    def std_dev(self):
        return statistics.pstdev(self._metrics)
        

    



class TTMTrend(Sc2TrendAnalyzer):

    def __init__(self, metric):
        #base.init(metric)
        pass


