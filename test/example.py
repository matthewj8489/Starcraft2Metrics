import sc2reader
from sc2reader.engine.plugins import APMTracker#, SelectionTracker, ContextLoader, SupplyTracker
import supply
from supply import SupplyTracker
#sc2reader.engine.register_plugin(APMTracker())
#sc2reader.engine.register_plugin(SelectionTracker())
#sc2reader.engine.register_plugin(ContextLoader())
#sc2reader.engine.register_plugin(SupplyTracker())


#replay = sc2reader.load_replay("test_replays\\PVZ_ADEPT_BENCHMARK.SC2Replay")
replay = sc2reader.load_replay("test_replays\\Year Zero LE (9).SC2Replay")

units=set([obj.name for obj in replay.objects.values()])

units_of_type = {name: [] for name in units}
for obj in replay.objects.values():
    units_of_type[obj.name].append(obj)
    
	
event_names = set([event.name for event in replay.events])

events_of_type = {name: [] for name in event_names}
for event in replay.events:
    events_of_type[event.name].append(event)


unit_born_events = events_of_type["UnitBornEvent"]
player1_ube = list(filter(lambda ube: ube.control_pid == 1, unit_born_events))
p1_army_ube = list(filter(lambda ube: ube.unit.is_army, player1_ube))
#for ube in unit_born_events:
#    if ube.control_pid == 1:
#        print("{} created {} at second {}".format(ube.unit_controller,
#                                                  ube.unit,
#                                                  ube.second))

unit_init_events = events_of_type["UnitInitEvent"]
player1_uie = list(filter(lambda uie: uie.control_pid == 1, unit_init_events))
p1_army_uie = list(filter(lambda uie: uie.unit.is_army, player1_uie))
#for uie in unit_init_events:
#    if uie.control_pid == 1:
#        print("{} started creating {} at second {}".format(uie.unit_controller,
#                                                           uie.unit,
#                                                           uie.second))

unit_done_events = events_of_type["UnitDoneEvent"]
player1_ude = list(filter(lambda ude: ude.unit.owner.pid == 1, unit_done_events))
p1_army_ude = list(filter(lambda ude: ude.unit.is_army, player1_ude))
#for ude in unit_done_events:
#    print("{} finished".format(ude.unit))


basic_cmd_events = events_of_type["BasicCommandEvent"]
p1_bce = list(filter(lambda bce: bce.player.pid == 1, basic_cmd_events))
p1_halluc_bce = list(filter(lambda bce: 'Hallucinate' in bce.ability_name, p1_bce))

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

total_adepts_done = len(adept_done_events)
for ade in adept_done_events:
    total_adepts_done += 1


player_stats_events = events_of_type["PlayerStatsEvent"]
player1_stats_events = list(filter(lambda pse: pse.pid == 1, player_stats_events))
player2_stats_events = list(filter(lambda pse: pse.pid == 2, player_stats_events))
##for pse in player_stats_events:
##    if pse.pid == 1:
##        player1_stats_events.append(pse)
##    elif pse.pid == 2:
##        player2_stats_events.append(pse)

ude_units = {"cols": 0, "zeals": 0, "adepts": 0, "archs": 0, "stalks": 0, "sents": 0, "obs": 0}
for x in p1_army_ude:
    if x.unit.name == "Colossus":
        ude_units["cols"] += 1
    elif x.unit.name == "Zealot":
        ude_units["zeals"] += 1
    elif x.unit.name == "Adept":
        ude_units["adepts"] += 1
    elif x.unit.name == "Archon":
        ude_units["archs"] += 1
    elif x.unit.name == "Stalker":
        ude_units["stalks"] += 1
    elif x.unit.name == "Sentry":
        ude_units["sents"] += 1
    elif x.unit.name == "Observer":
        ude_units["obs"] += 1

ube_units = {"cols": 0, "zeals": 0, "adepts": 0, "archs": 0, "stalks": 0, "sents": 0, "obs": 0}
for x in p1_army_ube:
    if x.unit.name == "Colossus":
        ube_units["cols"] += 1
    elif x.unit.name == "Zealot":
        ube_units["zeals"] += 1
    elif x.unit.name == "Adept":
        ube_units["adepts"] += 1
    elif x.unit.name == "Archon":
        ube_units["archs"] += 1
    elif x.unit.name == "Stalker":
        ube_units["stalks"] += 1
    elif x.unit.name == "Sentry":
        ube_units["sents"] += 1
    elif x.unit.name == "Observer":
        ube_units["obs"] += 1

uie_units = {"cols": 0, "zeals": 0, "adepts": 0, "archs": 0, "stalks": 0, "sents": 0, "obs": 0}
for x in p1_army_uie:
    if x.unit.name == "Colossus":
        uie_units["cols"] += 1
    elif x.unit.name == "Zealot":
        uie_units["zeals"] += 1
    elif x.unit.name == "Adept":
        uie_units["adepts"] += 1
    elif x.unit.name == "Archon":
        uie_units["archs"] += 1
    elif x.unit.name == "Stalker":
        uie_units["stalks"] += 1
    elif x.unit.name == "Sentry":
        uie_units["sents"] += 1
    elif x.unit.name == "Observer":
        uie_units["obs"] += 1

col_events = []
for x in p1_army_ube:
    if x.unit.name == "Colossus":
        col_events.append(x)

for x in p1_army_uie:
    if x.unit.name == "Colossus":
        col_events.append(x)
		
#print("Total Adepts Born ({})".format(total_adepts_born))        
#print("Total Adepts Init ({})".format(total_adepts_init))
#print("Total Adepts Done ({})".format(total_adepts_done))        

replay.is_ladder
replay.map_name
replay.humans
replay.computers
total_players = len(replay.humans) + len(replay.computers)
total_players
