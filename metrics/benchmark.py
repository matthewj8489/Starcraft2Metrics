import sc2reader
import util

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

    workers = worker_created_benchmark(events_dictionary, player_id, game_bench_time_s)
    army = army_created_benchmark(events_dictionary, player_id, game_bench_time_s)
    total_supply_created = workers + army
    replay_time_measured = min(benchmark_time_s, replay.game_length.seconds)
    
    return {'BenchmarkLength': replay_time_measured, 'TotalSupply': total_supply_created, 'Workers': workers, 'Army': army}



########## PRIVATE ###########
def worker_created_benchmark(event_dict, player_id, benchmark_time_s):
    if not 'UnitBornEvent' in event_dict:
        return 0
    unit_born_events = event_dict['UnitBornEvent']
    worker_count = 0

    for ube in unit_born_events:
        if ube.control_pid == player_id:
            if ube.unit.is_worker and ube.second <= benchmark_time_s:
                worker_count += ube.unit.supply

    return worker_count


def army_created_benchmark(event_dict, player_id, benchmark_time_s):
    if not 'UnitBornEvent' in event_dict or not 'UnitInitEvent' in event_dict:
        return 0
    unit_born_events = event_dict['UnitBornEvent']
    unit_init_events = event_dict['UnitInitEvent']   
    army_supply_count = 0

    player_ube = list(filter(lambda ube: ube.control_pid == player_id, unit_born_events))
    player_army_ube = list(filter(lambda ube: ube.unit.is_army, player_ube))

    for ube in player_army_ube:
        if (ube.second <= benchmark_time_s) and (ube.unit.name != "Archon") and (not ube.unit.hallucinated):
            army_supply_count += ube.unit.supply

    player_uie = list(filter(lambda uie: uie.control_pid == player_id, unit_init_events))
    player_army_uie = list(filter(lambda uie: uie.unit.is_army, player_uie))

    for uie in player_army_uie:
        if (uie.second <= benchmark_time_s) and (uie.unit.name != "Archon") and (not uie.unit.hallucinated):
            army_supply_count += uie.unit.supply

    return army_supply_count

def supply_available_benchmark(event_dict, player_id, benchmark_time_s):
    supply_count = 0

    return supply_count

def bases_completed_benchmark(event_dict, player_id, benchmark_time_s):
    bases_completed = 0

    return bases_completed

def minerals_mined_benchmark(event_dict, player_id, benchmark_time_s):
    minerals_mined = 0

    return minerals_mined

def gas_mined_benchmark(event_dict, player_id, benchmark_time_s):
    gas_mined = 0

    return gas_mined

def units_created(event_dict, player_id, benchmark_time_s):
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
        if (ube.second <= benchmark_time_s) and (ube.unit.name in units_created) and (ube.unit.hallucinated == False):
            units_created[ube.unit.name] += 1

    for uie in player_uie:
        if (uie.second <= benchmark_time_s) and (uie.unit.name in units_created) and (uie.unit.hallucinated == False):
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

    workers = worker_created_benchmark(events_dictionary, 1, bench_time_s)
    army = army_created_benchmark(events_dictionary, 1, bench_time_s)
    unit_dict = units_created(events_dictionary, 1, bench_time_s)

    bench_dict = benchmark("..\\test\\test_replays\\Year Zero LE (9).SC2Replay", 1, 618)
