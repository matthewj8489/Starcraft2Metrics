from collections import defaultdict
import math

from metrics.sc2metric import Sc2MetricAnalyzer
from metrics.metric_containers import FoodCount
from metrics.util import convert_gametime_to_realtime_r

        
class SupplyTracker(object):
    """
    Builds ``player.metrics.supply`` array made of :class:`~metrics.metric_containers.FoodCount`. 
    The ``metrics`` being of the type :class:`~metrics.sc2metric.Sc2MetricAnalyzer`. The supply 
    is tracked every time a new supply unit or supply building is made or dies/is destroyed.
    """

    name = 'SupplyTracker'

##    def _add_to_units_alive(self,event,replay):
##        self._units_alive[event.control_pid] += event.unit.supply
##        replay.player[event.control_pid].metrics.supply.append(
##            FoodCount(convert_gametime_to_realtime_r(replay, event.second),
##                      self._units_alive[event.control_pid],
##                      self._supply_gen[event.control_pid]))
##
##
##    def _add_to_supply_gen(self,event,replay):
##        self._supply_gen[event.unit.owner.pid] += self.supply_gen_unit[event.unit.name] #math.fabs(event.unit.supply)
##        replay.player[event.unit.owner.pid].metrics.supply.append(
##            FoodCount(convert_gametime_to_realtime_r(replay, event.second),
##                      self._units_alive[event.unit.owner.pid],
##                      self._supply_gen[event.unit.owner.pid]))
##        
##
##    def _remove_from_units_alive(self,event,replay):
##        self._units_alive[event.unit.owner.pid] -= event.unit.supply
##        replay.player[event.unit.owner.pid].metrics.supply.append(
##            FoodCount(convert_gametime_to_realtime_r(replay, event.second),
##                      self._units_alive[event.unit.owner.pid],
##                      self._supply_gen[event.unit.owner.pid]))
##        
##
##    def _remove_from_supply_gen(self,event,replay):
##        self._supply_gen[event.unit.owner.pid] -= self.supply_gen_unit[event.unit.name] #math.fabs(event.unit.supply)
##        replay.player[event.unit.owner.pid].metrics.supply.append(
##            FoodCount(convert_gametime_to_realtime_r(replay, event.second),
##                      self._units_alive[event.unit.owner.pid],
##                      self._supply_gen[event.unit.owner.pid]))
        
        
    def _add_to_units_alive(self, metrics, pid, supply, second):
        self._units_alive[pid] += supply
        metrics.supply.append(FoodCount(second,
                                        self._units_alive[pid],
                                        self._supply_gen[pid]))
        
    
    def _add_to_supply_gen(self, metrics, pid, supply, second):
        self._supply_gen[pid] += supply
        metrics.supply.append(FoodCount(second,
                                        self._units_alive[pid],
                                        self._supply_gen[pid]))
                                        
                                        
    def _remove_from_units_alive(self, metrics, pid, supply, second):
        self._units_alive[pid] -= supply
        metrics.supply.append(FoodCount(second,
                                        self._units_alive[pid],
                                        self._supply_gen[pid]))
                                        
                                        
    def _remove_from_supply_gen(self, metrics, pid, supply, second):
        self._supply_gen[pid] += supply
        metrics.supply.append(FoodCount(second,
                                        self._units_alive[pid],
                                        self._supply_gen[pid]))
                                        
                                        
    def _add_to_archon_debt(self):
        self._archon_debt += 2
        
    def _remove_one_templar_archon_debt(self):
        if self._archon_debt > 0:
            self._archon_debt -= 1
            
    def _handle_hallucination(self, unit_name):
        # if the unit name is found in the hallucinated list, this will
        # remove it from that list.
        # returns whether or not the unit was in the hallucination list
        for halluc in self._hallucinations:
            if unit_name in halluc:
                self._hallucinations.remove(halluc)
                return True
                
        return False
        
                                        
    def handleInitGame(self, event, replay):
        self.supply_gen_unit = {
            #'Overloard' : 8,
            #'Hatchery' : 2,
            #'SupplyDepot' : 8,
            #'CommandCenter' : 11,
            'Pylon' : 8,
            'Nexus' : 15
        }
        self.hallucinations = {
            'Probe' : 3,
            'Zealot' : 2,
            'Adept' : 2,
            'Stalker' : 2,
            'Immortal' : 1,
            'HighTemplar' : 2,
            'Archon' : 1,
            'VoidRay' : 1,
            'Phoenix' : 1,
            'WarpPrism' : 1,
            'Colossus' : 1
        }
        self._archon_debt = 0
        #self._hallucinations = []
        self._units_tracked = defaultdict(int)
        self._units_alive = defaultdict(int)
        self._supply_gen = defaultdict(int)

        for player in replay.players:
            self._units_tracked[player.pid] = []
            self._units_alive[player.pid] = 0
            self._supply_gen[player.pid] = 0
            player.metrics = Sc2MetricAnalyzer()


##    def handleUnitInitEvent(self,event,replay):
##        if event.unit.is_worker or (event.unit.is_army and not event.unit.hallucinated):
##            if (event.unit.name == 'Archon'):
##                self._add_to_archon_debt()
##            else:
##                self._add_to_units_alive(event,replay)
##            #self.add_to_units_alive(replay.player[event.control_pid].metrics, event.control_pid,
##            #                        event.unit.supply, event.second * replay.game_to_real_time_multiplier)
##
##
##    def handleUnitBornEvent(self,event,replay):
##        if event.unit.is_worker or (event.unit.is_army and not self._handle_hallucination(event.unit.name)):
##            self._add_to_units_alive(event,replay)
##        elif event.unit.is_building and (event.unit.name in self.supply_gen_unit):
##            self._add_to_supply_gen(event,replay)
##
##
##    def handleUnitDoneEvent(self,event,replay):
##        if event.unit.is_building and (event.unit.name in self.supply_gen_unit): #and event.unit.supply != 0:
##            self._add_to_supply_gen(event,replay)
##
##
##    def handleUnitDiedEvent(self,event,replay):
##        if event.unit.is_worker or (event.unit.is_army and not event.unit.hallucinated):
##            if (event.unit.name == 'HighTemplar' or event.unit.name == 'DarkTemplar') and self._archon_debt > 0:
##                self._remove_one_templar_archon_debt()
##            else:
##                self._remove_from_units_alive(event,replay)
##        elif event.unit.is_building and (event.unit.name in self.supply_gen_unit): #and event.unit.supply != 0:
##            self._remove_from_supply_gen(event,replay)
##
##
##    def handleCommandEvent(self,event,replay):
##        # apparently, the unitbornevent occurs for hallucinated units before the hallucinate command is even given...
##        #if ('Hallucinate' in event.ability_name):
##        #    print(event.ability_name)
##        #    self._hallucinations.append(event.ability_name)
##        pass
        
    class UnitTracker(object):
        def __init__(self, second, unit_name, supply, is_created, is_bldg):
            self.second = second
            self.unit_name = unit_name
            self.supply = supply
            self.is_created = is_created
            self.is_building = is_bldg
            
    #self._archon_debt = 0
    #self._units_tracked = []
        
        
    def handleUnitInitEvent(self,event,replay):
        if event.unit.is_worker or event.unit.is_army:
            if event.unit.name == 'Archon':
                self._archon_debt += 2
            else:
                self._units_tracked[event.unit.owner.pid].append(SupplyTracker.UnitTracker(convert_gametime_to_realtime_r(replay, event.second),
                                                       event.unit.name,
                                                       event.unit.supply,
                                                       True,
                                                       False))
                                                       
        
    def handleUnitBornEvent(self,event,replay):
        if event.unit.is_worker or event.unit.is_army or (event.unit.is_building and (event.unit.name in self.supply_gen_unit)):
            supply = 0
            if event.unit.is_building:
                supply = self.supply_gen_unit[event.unit.name]
            else:
                supply = event.unit.supply
            self._units_tracked[event.unit.owner.pid].append(SupplyTracker.UnitTracker(convert_gametime_to_realtime_r(replay, event.second),
                                                   event.unit.name,
                                                   supply,
                                                   True,
                                                   event.unit.is_building))
        
    
    def handleUnitDoneEvent(self,event,replay):
        if event.unit.is_building and (event.unit.name in self.supply_gen_unit):
            self._units_tracked[event.unit.owner.pid].append(SupplyTracker.UnitTracker(convert_gametime_to_realtime_r(replay, event.second),
                                                   event.unit.name,
                                                   self.supply_gen_unit[event.unit.name],
                                                   True,
                                                   True))
                                                   
        
    def handleUnitDiedEvent(self,event,replay):
        if event.unit.is_worker or event.unit.is_army or (event.unit.is_building and (event.unit.name in self.supply_gen_unit)):
            if self._archon_debt > 0 and (event.unit.name == 'HighTemplar' or event.unit.name == 'DarkTemplar'):
                self._archon_debt -= 1
            else:
                supply = 0
                if event.unit.is_building:
                    supply = self.supply_gen_unit[event.unit.name]
                else:
                    supply = event.unit.supply
                self._units_tracked[event.unit.owner.pid].append(SupplyTracker.UnitTracker(convert_gametime_to_realtime_r(replay, event.second),
                                                       event.unit.name,
                                                       supply,
                                                       False,
                                                       event.unit.is_building))
        
    
    def handleCommandEvent(self,event,replay):
        if ('Hallucinate' in event.ability_name):
            # remove the last unit tracked of that name
            unit_name = event.ability_name[11:]
            for j in range(self.hallucinations[unit_name]):
                for i in reversed(range(len(self._units_tracked[event.player.pid]))):
                    if self._units_tracked[event.player.pid][i].unit_name == unit_name:
                        del self._units_tracked[event.player.pid][i]
                        break
                
            
    
    def handleEndGame(self,event,replay):
        # process the supplies for the units tracked
        for plyr in replay.players:
            for ut in self._units_tracked[plyr.pid]:
                if ut.is_created:
                    if ut.is_building:
                        self._add_to_supply_gen(plyr.metrics, plyr.pid, ut.supply, ut.second)
                    else:
                        self._add_to_units_alive(plyr.metrics, plyr.pid, ut.supply, ut.second)
                else:
                    if ut.is_building:
                        self._remove_from_supply_gen(plyr.metrics, plyr.pid, ut.supply, ut.second)
                    else:
                        self._remove_from_units_alive(plyr.metrics, plyr.pid, ut.supply, ut.second)
                        
        
##    class UnitTracker(object):
##        def __init__(self, second, created, died, supply, is_bldg):
##            self.second = second
##            self.created = created
##            self.died = died
##            self.supply = supply
##            self.is_building = is_bldg
##            
##        
##    def handleEndGame(self,event,replay):
##        for plyr in replay.players:
##            unit_tracker = []
##            for ut in plyr.units:
##                if (ut.is_worker or (ut.is_army and not ut.hallucinated)):
##                    unit_tracker.append(UnitTracker(convert_frame_to_realtime_r(replay,ut.started_at), True, False, ut.supply, False))
##                    if ut.died_at > 0:
##                        unit_tracker.append(UnitTracker(convert_frame_to_realtime_r(replay,ut.died_at), False, True, ut.supply, False))
##                elif (ut.is_building and (event.unit.name in self.supply_gen_unit)):
##                    unit_tracker.append(UnitTracker(convert_frame_to_realtime_r(replay,ut.started_at), True, False, self.supply_gen_unit[event.unit.name], True)
##                    if ut.died_at > 0:
##                        unit_tracker.append(UnitTracker(convert_frame_to_realtime_r(replay,ut.died_at), False, True, self.supply_gen_unit[event.unit.name], True)
##            
##            unit_tracker.sort(key=lambda x: x.second)
##            
##            for trk in unit_tracker:
##                if trk.created:
##                    if trk.is_building:
##                        self._add_to_supply_gen(plyr.metrics, plyr.pid, trk.supply, trk.second)
##                    else:
##                        self._add_to_units_alive(plyr.metrics, plyr.pid, trk.supply, trk.second)
##                elif trk.died:
##                    if trk.is_building:
##                        self._remove_from_supply_gen(plyr.metrics, plyr.pid, trk.supply, trk.second)
##                    else:
##                        self._remove_from_units_alive(plyr.metrics, plyr.pid, trk.supply, trk.second)
##                        
##
##    def _isHallucinated(self, unit):
##        ################ bug : for whatever reason hallucinated attribute does not return correctly, it seems flags == 0 indicates hallucination (but only applies for army ########################
##        #return unit.hallucinated
##        return not ((unit.is_army and unit.flags != 0) or unit.is_worker)
