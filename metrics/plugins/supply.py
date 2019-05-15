from collections import defaultdict
import math

from metrics.sc2metric import Sc2MetricAnalyzer
from metrics.metric_containers import FoodCount
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
        
                    
    def _generate_accumulated_FoodCount(self, dict_units, dict_bldgs):
        new_units_lst = []
        new_bldgs_lst = []
        
        accsum = 0
        for key in dict_units:
            accsum += dict_units[key]
            new_units_lst.append(FoodCount(key, accsum, -1))
            
        accsum = 0
        for key in dict_bldgs:
            accsum += dict_bldgs[key]
            new_bldgs_lst.append(FoodCount(key, -1, accsum))
            
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
            sup_bldgs = defaultdict(int)
            
            # traverse units to track created and died
            filtered_units = list(filter(lambda x: (not x.hallucinated) and (not x.is_building), plyr.units))
            for unit in filtered_units:
                units[convert_frame_to_realtime_r(replay, unit.started_at)] += unit.supply
                units[convert_frame_to_realtime_r(replay, unit.died_at)] -= unit.supply
                
            # traverse supply buildings to track created and died
            filtered_bldgs = list(filter(lambda x: (x.is_building) and (x.name in self.supply_gen_unit), plyr.units))
            for unit in filtered_bldgs:
                sup_bldgs[convert_frame_to_realtime_r(replay, unit.started_at)] += self.supply_gen_unit[unit.name]
                sup_bldgs[convert_frame_to_realtime_r(replay, unit.died_at)] -= self.supply_gen_unit[unit.name]
    
            plyr.metrics.supply = self._generate_accumulated_FoodCount(units, sup_bldgs)
            
            