import sc2reader
import util

class Benchmark(object):
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


    def time_to_66_workers(self):
        if not 'UnitBornEvent' in self._events:
            return 0

        unit_born_events = self._events['UnitBornEvent']
        worker_count = 0

        for ube in unit_born_events:
            if (ube.control_pid == self._player_id) and (ube.unit.is_worker):
                worker_count += 1
                if worker_count >= 66:
                    return util.convert_gametime_to_realtime_r(self._replay, ube.second)

        return -1






def benchmark(replay_file, player_id, benchmark_time_s):
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
    'SupplyBlocked' : Time spent supply blocked.
    'SQ' : Spending quotient.
    'AvgAPM' : Average APM
    'AvgSPM' : Average SPM
    'Units' : Dictionary of all the units created, keyed by the units' names.
    '''
    
    replay = sc2reader.load_replay(replay_file)

    event_names = set([event.name for event in replay.events])
    events_dictionary = {name: [] for name in event_names}
    for event in replay.events:
        events_dictionary[event.name].append(event)

    game_bench_time_s = util.convert_realtime_to_gametime_r(replay, benchmark_time_s)

    workers = workers_created(events_dictionary, player_id, game_bench_time_s)
    army = army_created(events_dictionary, player_id, game_bench_time_s)
    total_supply_created = workers + army
    replay_time_measured = min(benchmark_time_s, replay.game_length.seconds)
    
    return {'BenchmarkLength': replay_time_measured, 'TotalSupply': total_supply_created, 'Workers': workers, 'Army': army}



########## PRIVATE ###########
def workers_created(event_dict, player_id, game_time_s):
    if not 'UnitBornEvent' in event_dict:
        return 0
    unit_born_events = event_dict['UnitBornEvent']
    worker_count = 0

    for ube in unit_born_events:
        if ube.control_pid == player_id:
            if ube.unit.is_worker and ube.second <= game_time_s:
                worker_count += ube.unit.supply

    return worker_count


def army_created(event_dict, player_id, game_time_s):
    if not 'UnitBornEvent' in event_dict or not 'UnitInitEvent' in event_dict:
        return 0
    unit_born_events = event_dict['UnitBornEvent']
    unit_init_events = event_dict['UnitInitEvent']   
    army_supply_count = 0

    player_ube = list(filter(lambda ube: ube.control_pid == player_id, unit_born_events))
    player_army_ube = list(filter(lambda ube: ube.unit.is_army, player_ube))

    for ube in player_army_ube:
        if (ube.second <= game_time_s) and (ube.unit.name != "Archon") and (not ube.unit.hallucinated):
            army_supply_count += ube.unit.supply

    player_uie = list(filter(lambda uie: uie.control_pid == player_id, unit_init_events))
    player_army_uie = list(filter(lambda uie: uie.unit.is_army, player_uie))

    for uie in player_army_uie:
        if (uie.second <= game_time_s) and (uie.unit.name != "Archon") and (not uie.unit.hallucinated):
            army_supply_count += uie.unit.supply

    return army_supply_count


def time_to_66_workers(event_dict, player_id):
    if not 'UnitBornEvent' in event_dict:
        return 0

    unit_born_events = event_dict['UnitBornEvent']
    worker_count = 0

    for ube in unit_born_events:
        if (ube.control_pid == player_id) and (ube.unit.is_worker):
            worker_count += 1
            if workert_count >= 66:
                return ube.second


def units_created(event_dict, player_id, game_time_s):
    if not 'UnitBornEvent' in event_dict or not 'UnitInitEvent' in event_dict:
        return 0
    units_created = {"Probe": 0, "Zealot": 0, "Sentry": 0, "Stalker": 0, "Adept": 0, "HighTemplar": 0,
                     "DarkTemplar": 0, "Archon": 0, "Observer": 0, "Immortal": 0, "Colossus": 0,
                     "Disruptor": 0, "Phoenix": 0, "Oracle": 0, "VoidRay": 0, "Carrier": 0, "Tempest": 0}

    unit_born_events = event_dict['UnitBornEvent']
    unit_init_events = event_dict['UnitInitEvent']   
    
    player_ube = list(filter(lambda ube: ube.control_pid == player_id, unit_born_events))
    player_uie = list(filter(lambda uie: uie.control_pid == player_id, unit_init_events))

    for ube in player_ube:
        if (ube.second <= game_time_s) and (ube.unit.name in units_created) and (ube.unit.hallucinated == False):
            units_created[ube.unit.name] += 1

    for uie in player_uie:
        if (uie.second <= game_time_s) and (uie.unit.name in units_created) and (uie.unit.hallucinated == False):
            units_created[uie.unit.name] += 1

    return units_created
    

########## Testing ###########
if __name__ == '__main__':
    replay = sc2reader.load_replay("..\\test\\test_replays\\Year Zero LE (9).SC2Replay")

    event_names = set([event.name for event in replay.events])
    events_dictionary = {name: [] for name in event_names}
    for event in replay.events:
        events_dictionary[event.name].append(event)

    bench_time_s = util.convert_realtime_to_gametime_r(replay, 618)

    workers = worker_created(events_dictionary, 1, bench_time_s)
    army = army_created(events_dictionary, 1, bench_time_s)
    unit_dict = units_created(events_dictionary, 1, bench_time_s)

    bench_dict = benchmark("..\\test\\test_replays\\Year Zero LE (9).SC2Replay", 1, 618)
