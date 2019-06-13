from collections import defaultdict
import math

from metrics.sc2metric import Sc2MetricAnalyzer
from metrics.metric_containers import FoodCount
from metrics.metric_containers import SupplyCount
from metrics.util import convert_frame_to_realtime_r

        
class SupplyTracker(object):
    """
    Builds ``player.metrics.supply`` array made of :class:`~metrics.metric_containers.FoodCount`. 
    The ``metrics`` being of the type :class:`~metrics.sc2metric.Sc2MetricAnalyzer`. The supply 
    is tracked every time a new supply unit or supply building is made or dies/is destroyed.
    """

    name = 'SupplyTracker'

    def __init__(self):
        self.supply_gen_unit = {
            #'Overloard' : 8,
            #'Hatchery' : 2,
            #'SupplyDepot' : 8,
            #'CommandCenter' : 11,
            'Pylon' : 8,
            'Nexus' : 15
        }
        self.train_time = {
            'Probe' : 12,
            'Zealot' : 27,
            'Adept' : 30,
            'Stalker' : 30,
            'HighTemplar' : 39,
            'DarkTemplar' : 39,
            'Sentry' : 26,
            'Observer' : 21,
            'Immortal' : 39,
            'Colossus' : 54,
            'Disruptor' : 36,
            'Phoenix' : 25,
            'Oracle' : 37,
            'VoidRay' : 43,
            'Carrier' : 64,
            'Tempest' : 43            
        }
        
                    
    def _generate_accumulated_FoodCount(self, dict_units, dict_bldgs):
        new_units_lst = []
        new_bldgs_lst = []
        
        for key in dict_units:
            new_units_lst.append(FoodCount(key, dict_units[key], -1))
            
        new_units_lst = sorted(new_units_lst, key=lambda x: x.second)
        
        accsum = 0
        for ut in new_units_lst:
            accsum += ut.supply_used
            ut.supply_used = accsum
        
        for key in dict_bldgs:
            new_bldgs_lst.append(FoodCount(key, -1, dict_bldgs[key]))
            
        new_bldgs_lst = sorted(new_bldgs_lst, key=lambda x: x.second)
            
        accsum = 0
        for bd in new_bldgs_lst:
            accsum += bd.supply_made
            bd.supply_made = accsum
        
        #accsum = 0
        #for key in dict_units:
        #    accsum += dict_units[key]
        #    new_units_lst.append(FoodCount(key, accsum, -1))
            
        #accsum = 0
        #for key in dict_bldgs:
        #    accsum += dict_bldgs[key]
        #    new_bldgs_lst.append(FoodCount(key, -1, accsum))
            
        # combine entries occurring at the same time               
        for unit in new_units_lst:
            matches = list(filter(lambda x: x.second == unit.second, new_bldgs_lst))
            if len(matches) > 0:
                unit.supply_made = matches[0].supply_made
                new_bldgs_lst.remove(matches[0])
            
        # combine the lists and sort them by second
        new_lst = sorted(new_units_lst + new_bldgs_lst, key=lambda x: x.second)
        
        last_sup_used = 0
        last_sup_made = 0
        for itm in new_lst:
            if itm.supply_used >= 0:
                last_sup_used = itm.supply_used
            else:
                itm.supply_used = last_sup_used
                
            if itm.supply_made >= 0:
                last_sup_made = itm.supply_made
            else:
                itm.supply_made = last_sup_made
                
        return new_lst
        
    
    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.metrics = Sc2MetricAnalyzer()
    
    
    def handleEndGame(self,event,replay):   
        for plyr in replay.players:
            units = defaultdict(int)
            units_created_sum = 0
            units_created_only = []
            army_created_sum = 0
            army_created = []
            workers_created_sum = 0
            workers_created = []
            sup_bldgs = defaultdict(int)
            
            # traverse units to track created and died
            filtered_units = list(filter(lambda x: (not x.hallucinated) and (x.is_worker or x.is_army), plyr.units))
            for unit in filtered_units:
                if unit.started_at == unit.finished_at:
                    # need to account for the fact that units that are training, but not yet 'born', still take up supply
                    # a decent alternative - build independent - approach would be the following:
                    # add each BasicCommandEvent.second that is a 'TrainXYZ' command to a stack for each 'XYZ' unit.
                    # when a UnitBornEvent occurs, pop that time off of the corresponding stack, and add it to a new attribute
                    # called unit_trained_at (it may be inaccurate as to which unit the command event actually ties to, but
                    # for supply, this doesn't matter). 
                    # Now, in this method, when unit_trained_at is not None, use that attribute as the time it got started.
                    # NOTE: this won't really account for starting a training unit, then canceling it before it finishes, but
                    # whatever.
                    start_time = convert_frame_to_realtime_r(replay, unit.started_at) - self.train_time[unit.name]
                    created_time = convert_frame_to_realtime_r(replay, unit.started_at)
                    if start_time < 0:
                        start_time = 0
                    units[start_time] += unit.supply
                    units_created_sum += unit.supply
                    units_created_only.append(SupplyCount(created_time, units_created_sum, unit.supply, unit.is_worker))
                    if unit.is_worker:
                        workers_created_sum += unit.supply
                        workers_created.append(SupplyCount(created_time, workers_created_sum, unit.supply, unit.is_worker))
                    else:
                        army_created_sum += unit.supply
                        army_created.append(SupplyCount(created_time, army_created_sum, unit.supply, unit.is_worker))
                else:
                    start_time = convert_frame_to_realtime_r(replay, unit.started_at)
                    units[start_time] += unit.supply
                    units_created_sum += unit.supply
                    units_created_only.append(SupplyCount(start_time, units_created_sum, unit.supply, unit.is_worker))
                    if unit.is_worker:
                        workers_created_sum += unit.supply
                        workers_created.append(SupplyCount(start_time, workers_created_sum, unit.supply, unit.is_worker))
                    else:
                        army_created_sum += unit.supply
                        army_created.append(SupplyCount(start_time, army_created_sum, unit.supply, unit.is_worker))
                if unit.died_at is not None:
                    units[convert_frame_to_realtime_r(replay, unit.died_at)] -= unit.supply
                
            # traverse supply buildings to track created and died
            filtered_bldgs = list(filter(lambda x: (x.is_building) and (x.name in self.supply_gen_unit), plyr.units))
            for unit in filtered_bldgs:
                if unit.finished_at is not None:
                    sup_bldgs[convert_frame_to_realtime_r(replay, unit.finished_at)] += self.supply_gen_unit[unit.name]
                if unit.died_at is not None:
                    sup_bldgs[convert_frame_to_realtime_r(replay, unit.died_at)] -= self.supply_gen_unit[unit.name]

            plyr.metrics.supply = self._generate_accumulated_FoodCount(units, sup_bldgs)
            plyr.metrics.supply_created = units_created_only
            plyr.metrics.workers_created = workers_created
            plyr.metrics.army_created = army_created
            
