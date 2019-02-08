import sc2reader




########## PRIVATE ###########
def worker_created_benchmark(event_dict, player_id, benchmark_time_s):
    unit_born_events = event_dict['UnitBornEvent']
    worker_count = 0

    for ube in unit_born_events:
        if ube.control_pid == player_id:
            if ube.unit.is_worker and ube.second <= benchmark_time_s:
                worker_count += 1

    return worker_count


def army_created_benchmark(event_dict, player_id, benchmark_time_s):
    unit_born_events = event_dict['UnitBornEvent']
    unit_init_events = event_dict['UnitInitEvent']
    army_supply_count = 0

    for ube in unit_born_events:
        if ube.control_pid == player_id:
            if ube.unit.is_army and ube.second <= benchmark_time_s:
                army_supply_count += ube.unit.supply

    for uie in unit_init_events:
        if uie.control_pid == player_id:
            if uie.unit.is_army and uie.second <= benchmark_time_s:
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

########## Testing ###########
replay = sc2reader.load_replay("..\\test\\test_replays\\PVZ_ADEPT_BENCHMARK.SC2Replay")

event_names = set([event.name for event in replay.events])
events_dictionary = {name: [] for name in event_names}
for event in replay.events:
    events_dictionary[event.name].append(event)

workers = worker_created_benchmark(events_dictionary, 1, 600)
army = army_created_benchmark(events_dictionary, 1, 600)
