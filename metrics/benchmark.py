import sc2reader

def benchmark(replay_file, player_id, benchmark_time_s):
    replay = sc2reader.load_replay(replay_file)

    event_names = set([event.name for event in replay.events])
    events_dictionary = {name: [] for name in event_names}
    for event in replay.events:
        events_dictionary[event.name].append(event)

    workers = worker_created_benchmark(events_dictionary, player_id, benchmark_time_s)
    army = army_created_benchmark(events_dictionary, player_id, benchmark_time_s)
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

##    for ube in unit_born_events:
##        if ube.control_pid == player_id:
##            if ube.unit.is_army and ube.second <= benchmark_time_s:
##                if (ube.unit.name != "Archon") and (ube.unit.hallucinated == False):
##                    army_supply_count += ube.unit.supply
##
##    for uie in unit_init_events:
##        if uie.control_pid == player_id:
##            if uie.unit.is_army and uie.second <= benchmark_time_s:
##                if (uie.unit.name != "Archon") and (uie.unit.hallucinated == False):
##                    army_supply_count += uie.unit.supply

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

    real_bench_time_s = 618
    real_fps = replay.frames / replay.game_length.seconds
    bench_frame = real_bench_time_s * real_fps
    bench_time_s = bench_frame // replay.game_fps

    #bench_time_s = 866

    workers = worker_created_benchmark(events_dictionary, 1, bench_time_s)
    army = army_created_benchmark(events_dictionary, 1, bench_time_s)
    unit_dict = units_created(events_dictionary, 1, bench_time_s)
