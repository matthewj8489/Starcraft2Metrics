import sc2reader

replay = sc2reader.load_replay("test_replays\\PVZ_ADEPT_BENCHMARK.SC2Replay")

event_names = set([event.name for event in replay.events])

events_of_type = {name: [] for name in event_names}
for event in replay.events:
    events_of_type[event.name].append(event)


unit_born_events = events_of_type["UnitBornEvent"]

#for ube in unit_born_events:
#    if ube.control_pid == 1:
#        print("{} created {} at second {}".format(ube.unit_controller,
#                                                  ube.unit,
#                                                  ube.second))

unit_init_events = events_of_type["UnitInitEvent"]

#for uie in unit_init_events:
#    if uie.control_pid == 1:
#        print("{} started creating {} at second {}".format(uie.unit_controller,
#                                                           uie.unit,
#                                                           uie.second))

unit_done_events = events_of_type["UnitDoneEvent"]

#for ude in unit_done_events:
#    print("{} finished".format(ude.unit))


adept_born_events = list(filter(lambda ube: ube.unit.name == "Adept", unit_born_events))

total_adepts_born = 0
for abe in adept_born_events:
    if abe.control_pid == 1:
        #print("{} created at second {}".format(abe.unit, abe.second))
        total_adepts_born += 1


adept_init_events = list(filter(lambda uie: uie.unit.name == "Adept", unit_init_events))

total_adepts_init = 0
for aie in adept_init_events:
    if aie.control_pid == 1:
        total_adepts_init += 1
        

adept_done_events = list(filter(lambda ude: ude.unit.name == "Adept", unit_done_events))

total_adepts_done = 0
for ade in adept_done_events:
    total_adepts_done += 1


player_stats_events = events_of_type["PlayerStatsEvent"]
player1_stats_events = []
player2_stats_events = []
for pse in player_stats_events:
    if pse.pid == 1:
        player1_stats_events.append(pse)
    elif pse.pid == 2:
        player2_stats_events.append(pse)


#print("Total Adepts Born ({})".format(total_adepts_born))        
#print("Total Adepts Init ({})".format(total_adepts_init))
#print("Total Adepts Done ({})".format(total_adepts_done))        
