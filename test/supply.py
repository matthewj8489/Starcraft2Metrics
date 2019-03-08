from collections import defaultdict
import math

class SupplyTracker(object):

    name = 'SupplyTracker'

    def add_to_units_alive(self,event,replay):
        self.units_alive[event.control_pid] += event.unit.supply
        replay.player[event.control_pid].current_food_used[event.second] = self.units_alive[event.control_pid]


    def add_to_supply_gen(self,event,replay):
        print("here")
        self.supply_gen[event.control_pid] += self.supply_gen_unit[event.unit.name] #math.fabs(event.unit.supply)
        replay.player[event.control_pid].current_food_made[event.second] = self.supply_gen[event.control_pid]
        

    def remove_from_units_alive(self,event,replay):
        self.units_alive[event.unit.owner.pid] -= event.unit.supply
        replay.player[event.unit.owner.pid].current_food_used[event.second] = self.units_alive[event.unit.owner.pid]
        

    def remove_from_supply_gen(self,event,replay):
        self.supply_gen[event.unit.owner.pid] -= self.supply_gen_unit[event.unit.name] #math.fabs(event.unit.supply)
        replay.player[event.unit.owner.pid].current_food_made[event.second] = self.supply_gen[event.unit.owner.pid]
        

    def handleInitGame(self, event, replay):
        self.supply_gen_unit = {
            'Overloard' : 8,
            'Hatchery' : 2,
            'SupplyDepot' : 8,
            'CommandCenter' : 11,
            'Pylon' : 8,
            'Nexus' : 10
        }
        self.units_alive = dict()
        self.supply_gen = dict()

        for player in replay.players:
            self.units_alive[player.pid] = 0
            self.supply_gen[player.pid] = 0
            player.current_food_used = defaultdict(int)
            player.current_food_made = defaultdict(int)                    


    def handleUnitInitEvent(self,event,replay):
        if event.unit.is_worker or event.unit.is_army and not event.unit.hallucinated:
            self.add_to_units_alive(event,replay)


    def handleUnitBornEvent(self,event,replay):
        if event.unit.is_worker or event.unit.is_army and not event.unit.hallucinated:
            self.add_to_units_alive(event,replay)


    def handleUnitDoneEvent(self,event,replay):
        if event.unit.is_building and (event.unit.name in self.supply_gen_unit): #and event.unit.supply != 0:
            self.add_to_supply_gen(event,replay)


    def handleUnitDiedEvent(self,event,replay):
        if event.unit.is_worker or event.unit.is_army and not event.unit.hallucinated:
            self.remove_from_units_alive(event,replay)
        elif event.unit.is_building and (event.unit.name in self.supply_gen_unit): #and event.unit.supply != 0:
            self.remove_from_supply_gen(event,replay)


    def handleEndGame(self, event, replay):
        for player in replay.players:
            player.current_food_used = sorted(player.current_food_used.items(), key=lambda x:x[0])
            player.current_food_made = sorted(player.current_food_made.items(), key=lambda x:x[0])
        
