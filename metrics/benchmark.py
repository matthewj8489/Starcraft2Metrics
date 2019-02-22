import sc2reader
import util

class Benchmark(object):
    '''
    Find benchmark metrics for the given replay file at the given real time.
    (Benchmarks include 'Total Supply Created', 'Workers Created', 'Army Created')

    Keyword arguments:
    replay_file -- the location of the replay to parse.
    player_id -- the id number of the player to monitor in the replay
    benchmark_time_s -- the real time of when to take the benchmark measurement

    Output:
    Dictionary containing the following keys:
    'BenchmarkLength' : Length of time measured in the benchmark, relevant if the replay was shorter than the benchmark_time_s parameter
    'TotalSupply' : Total supply created by the player. (This is NOT current supply at given time)
    'Workers' : Total number of workers created by the player.
    'Army' : Total army supply created by the player.
    'Upgrades' : Total count of upgrades. (+1/2/3 weapons, psionic storm, charge, etc.)
    'TimeTo66Probes' : Time at which the user created 66 probes (3-base saturation).
    'TimeTo75Probes' : Time at which the user created 75 probes.
    'TimeTo3Base' : Time at which a third base is finished.
    'TimeTo4Base' : Time at which a fourth base is finished.
    'TimeTo5Base' : Time at which a fifth base is finished.
    'TimeToSupply : Time at which the user created the specified supply.
    'SupplyBlocked' : Time spent supply blocked.
    'SQ' : Spending quotient.
    'AvgAPM' : Average APM
    'AvgSPM' : Average SPM
    'Units' : Dictionary of all the units created, keyed by the units' names.
    '''   

    
    def __init__(self, replay_file, player_id):
        #: Replay structure
        self._replay = sc2reader.load_replay(replay_file)

        #: An events dictionary from the replay
        event_names = set([event.name for event in self._replay.events])
        self._events = {name: [] for name in event_names}
        for event in self._replay.events:
            self._events[event.name].append(event)
         

        #: The ID of the player for whom to parse benchmark data
        self._player_id = player_id


    def workers_created(self, real_time_s):
        if not 'UnitBornEvent' in self._events:
            return 0
        unit_born_events = self._events['UnitBornEvent']
        worker_count = 0
        game_time_s = util.convert_realtime_to_gametime_r(self._replay, real_time_s)

        for ube in unit_born_events:
            if ube.control_pid == self._player_id:
                if ube.unit.is_worker and ube.second <= game_time_s:
                    worker_count += ube.unit.supply

        return worker_count


    def army_created(self, real_time_s):
        if not 'UnitBornEvent' in self._events or not 'UnitInitEvent' in self._events:
            return 0
        unit_born_events = self._events['UnitBornEvent']
        unit_init_events = self._events['UnitInitEvent']   
        army_supply_count = 0
        game_time_s = util.convert_realtime_to_gametime_r(self._replay, real_time_s)

        player_ube = list(filter(lambda ube: ube.control_pid == self._player_id, unit_born_events))
        player_army_ube = list(filter(lambda ube: ube.unit.is_army, player_ube))

        for ube in player_army_ube:
            if (ube.second <= game_time_s) and (ube.unit.name != "Archon") and (not ube.unit.hallucinated):
                army_supply_count += ube.unit.supply

        player_uie = list(filter(lambda uie: uie.control_pid == self._player_id, unit_init_events))
        player_army_uie = list(filter(lambda uie: uie.unit.is_army, player_uie))

        for uie in player_army_uie:
            if (uie.second <= game_time_s) and (uie.unit.name != "Archon") and (not uie.unit.hallucinated):
                army_supply_count += uie.unit.supply

        return army_supply_count


    def total_supply_created(self, real_time_s):
        supply = 0
        supply += self.workers_created(real_time_s)
        supply += self.army_created(real_time_s)

        return supply


    def time_to_worker_count(self, worker_count):
        if not 'UnitBornEvent' in self._events:
            return 0

        unit_born_events = self._events['UnitBornEvent']
        wc = 0

        for ube in unit_born_events:
            if (ube.control_pid == self._player_id) and (ube.unit.is_worker):
                wc += 1
                if wc >= worker_count:
                    return util.convert_gametime_to_realtime_r(self._replay, ube.second)

        return -1


    def time_to_66_workers(self):
        return self.time_to_worker_count(66)


    def time_to_supply_count(self, supply_count):
        # filter all the objects into just the units (workers + army) that were not hallucinated
        units = list(filter(lambda ut: ut.owner.pid == self._player_id and (ut.is_army or ut.is_worker) and (ut.hallucinated == False), self._replay.player[self._player_id].units))

        # filter out special cases, such as Archons that were morphed from templars
        units_r = list(filter(lambda ut: ut.name != "Archon", units))
                
        supp = 0
        for ut in units_r:
            supp += ut.supply
            if supp >= supply_count:
                return util.convert_frame_to_realtime_r(self._replay, ut.finished_at)

        return -1
        

    def units_created(self, real_time_s):
        if not 'UnitBornEvent' in self._events or not 'UnitInitEvent' in self._events:
            return 0
        units_created = {"Probe": 0, "Zealot": 0, "Sentry": 0, "Stalker": 0, "Adept": 0, "HighTemplar": 0,
                         "DarkTemplar": 0, "Archon": 0, "Observer": 0, "Immortal": 0, "Colossus": 0,
                         "Disruptor": 0, "Phoenix": 0, "Oracle": 0, "VoidRay": 0, "Carrier": 0, "Tempest": 0}

        unit_born_events = self._events['UnitBornEvent']
        unit_init_events = self._events['UnitInitEvent']
        game_time_s = util.convert_realtime_to_gametime_r(self._replay, real_time_s)
        
        player_ube = list(filter(lambda ube: ube.control_pid == self._player_id, unit_born_events))
        player_uie = list(filter(lambda uie: uie.control_pid == self._player_id, unit_init_events))

        for ube in player_ube:
            if (ube.second <= game_time_s) and (ube.unit.name in units_created) and (ube.unit.hallucinated == False):
                units_created[ube.unit.name] += 1

        for uie in player_uie:
            if (uie.second <= game_time_s) and (uie.unit.name in units_created) and (uie.unit.hallucinated == False):
                units_created[uie.unit.name] += 1

        return units_created


    def unit_list(self):
        if not 'UnitBornEvent' in self._events or not 'UnitInitEvent' in self._events:
            return 0
        
        unit_born_events = self._events['UnitBornEvent']
        unit_init_events = self._events['UnitInitEvent']

        player_ube = list(filter(lambda ube: ube.control_pid == self._player_id, unit_born_events))
        player_uie = list(filter(lambda uie: uie.control_pid == self._player_id, unit_init_events))

        unit_list = []

        for ube in player_ube:
            unit_list.append([ube.unit, ube.second])

        for uie in player_uie:
            unit_list.append([uie.unit, uie.second])



   
########## Testing ###########
if __name__ == '__main__':

    bc = Benchmark("..\\test\\test_replays\\Year Zero LE (9).SC2Replay", 1)
