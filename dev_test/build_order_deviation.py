import sc2reader


def build_order_deviation(bench_replay_location, player_replay_location, player_name):
    rep_bench = sc2reader.load_replay(bench_replay_location)
    rep_player = sc2reader.load_replay(player_replay_location)


    # retrieve the shortest game length between the two replays
    b_game_length = rep_bench.frames // rep_bench.game_fps
    p_game_length = rep_player.frames // rep_player.game_fps
    min_game_length = min(b_game_length, p_game_length)


    # determine the pid of the player testing the BO deviation
    bench_pid = 0
    if rep_bench.players[0].name == player_name:
        bench_pid = rep_bench.players[0].pid
    else:
        bench_pid = rep_bench.players[1].pid

    rep_pid = 0
    if rep_player.players[0].name == player_name:
        rep_pid = rep_player.players[0].pid
    else:
        rep_pid = rep_player.players[1].pid 


    # create a dictionary of events
    bench_event_names = set([event.name for event in rep_bench.events])
    bench_events_of_type = {name: [] for name in bench_event_names}
    for event in rep_bench.events:
        bench_events_of_type[event.name].append(event)
    bench_unit_born_events = bench_events_of_type["UnitBornEvent"]       
    bench_unit_init_events = bench_events_of_type["UnitInitEvent"]

    rep_event_names = set([event.name for event in rep_player.events])
    rep_events_of_type = {name: [] for name in rep_event_names}
    for event in rep_player.events:
        rep_events_of_type[event.name].append(event)
    rep_unit_born_events = rep_events_of_type["UnitBornEvent"]
    rep_unit_init_events = rep_events_of_type["UnitInitEvent"]

    bench_player_ube = list(filter(lambda evt: evt.control_pid == bench_pid, bench_unit_born_events))
    bench_player_uie = list(filter(lambda evt: evt.control_pid == bench_pid, bench_unit_init_events))
    replay_player_ube = list(filter(lambda evt: evt.control_pid == rep_pid, rep_unit_born_events))
    replay_player_uie = list(filter(lambda evt: evt.control_pid == rep_pid, rep_unit_init_events))      


    # Find all units created (worker, army, building)
    bench_units_created = dict()
    bench_units_created['worker'] = []
    for ube in bench_player_ube:
        if ube.unit.is_worker:
            bench_units_created['worker'].append(ube.second)
        if ube.unit.is_army:
            if not ube.unit.name in bench_units_created:
                bench_units_created[ube.unit.name] = []
            bench_units_created[ube.unit.name].append(ube.second)

    for uie in bench_player_uie:
        if uie.unit.is_army:
            if not uie.unit.name in bench_units_created:
                bench_units_created[uie.unit.name] = []
            bench_units_created[uie.unit.name].append(uie.second)

    replay_units_created = dict()
    replay_units_created['worker'] = []
    for ube in replay_player_ube:
        if ube.unit.is_worker:
            replay_units_created['worker'].append(ube.second)
        if ube.unit.is_army:
            if not ube.unit.name in replay_units_created:
                replay_units_created[ube.unit.name] = []
            replay_units_created[ube.unit.name].append(ube.second)

    for uie in replay_player_uie:
        if uie.unit.is_army:
            if not uie.unit.name in replay_units_created:
                replay_units_created[uie.unit.name] = []
            replay_units_created[uie.unit.name].append(uie.second)


    # Calculate the BOD for each unit
    BODu = dict()
    for unit_created in bench_units_created:
        if unit_created in replay_units_created:
            BODu[unit_created] = BOD(bench_units_created[unit_created], replay_units_created[unit_created], min_game_length)

    # Print results
    for bod_unit in BODu:
        print("BOD({}) : {} s/u".format(bod_unit, BODu[bod_unit]))
        

  
#### PRIVATE FUNCTIONS ####
def unit_compare(benchmark, player):
    compare = []
    total = min(len(benchmark), len(player))
    for x in range(total):
        compare.append(benchmark[x] - player[x])

    return compare


def filter_on_game_length(rep_units, game_length):
    rep_units_filter = list(filter(lambda tm: tm <= game_length, rep_units))
    return rep_units_filter


def BOD(bench_units, player_units, game_length):
    bench_units_filter = filter_on_game_length(bench_units, game_length)
    player_units_filter = filter_on_game_length(player_units, game_length)

    unit_comp = unit_compare(bench_units_filter, player_units_filter)

    if len(unit_comp) == 0:
        return -1

    w_sum_abs = 0
    for x in range(len(unit_comp)):
        w_sum_abs += abs(unit_comp[x])

    return w_sum_abs / len(unit_comp)


def DEV(bench_units, player_units, game_length):
    bench_units_filter = filter_on_game_length(bench_units, game_length)
    player_units_filter = filter_on_game_length(player_units, game_length)

    unit_comp = unit_compare(bench_units_filter, player_units_filter)

    return unit_comp[len(unit_comp)-1]
