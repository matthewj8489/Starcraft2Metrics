import sc2reader


def build_order_deviation(bench_replay_location, player_replay_location):
    rep_bench = sc2reader.load_replay(bench_replay_location)
    rep_player = sc2reader.load_replay(player_replay_location)

    # retrieve the shortest game length between the two replays
    b_game_length = rep_bench.frames // rep_bench.game_fps
    p_game_length = rep_player.frames // rep_player.game_fps
    min_game_length = min(b_game_length, p_game_length)

    # create a dictionary of events
    event_names = set([event.name for event in replay.events])
    events_of_type = (name: [] for name in event_names)
    unit_born_events = events_of_type["UnitBornEvent"]
    unit_init_events = events_of_type["UnitInitEvent"]

    # for each relevant unit (a unit that was created), calculate a BOD and DEV


  
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

    w_sum_abs = 0
    for x in range(len(unit_comp)):
        w_sum_abs += abs(unit_comp[x])

    return w_sum_abs / len(unit_comp)


def DEV(bench_units, player_units, game_length):
    bench_units_filter = filter_on_game_length(bench_units, game_length)
    player_units_filter = filter_on_game_length(player_units, game_length)

    unit_comp = unit_compare(bench_units_filter, player_units_filter)

    return unit_comp[len(unit_comp)-1]
