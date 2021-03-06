import sc2reader
import matplotlib.pyplot as plt
import numpy as np


def worker_created(replay, player_id):
    workers = []
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if event.unit.is_worker:
                workers.append(event.second)

    return workers


def adept_created(replay, player_id):
    adepts = []
    for event in replay.events:
        # UnitBornEvent for gateway spawned adepts, UnitInitEvent for warped-in adepts
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if event.unit.name == "Adept" or event.unit.name == "adept":
                adepts.append(event.second)
        elif event.name == "UnitInitEvent" and event.control_pid == player_id:
            if event.unit.name == "Adept" or event.unit.name == "adept":
                adepts.append(event.second)

    return adepts


def army_created(replay, player_id):
    army = []
    for event in replay.events:
        if event.name == "UnitBornEvent" and event.control_pid == player_id:
            if event.unit.is_army:
                army.append([event.second, event.unit.name])
        elif event.name == "UnitInitEvent" and event.control_pid == player_id:
            if event.unit.is_army:
                army.append([event.second, event.unit_name])

    return army


def unit_compare(benchmark, player):
    compare = []
    total = min(len(benchmark), len(player))
    for x in range(total):
        compare.append(benchmark[x] - player[x])

    return compare


def ROC(wp, total):
    roc = []
    x = 0
    while x < (total - 1):
        rocs = (wp[x+1] - wp[x])
        roc.append(rocs)
        x+=1

    return roc

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


rep_bench = sc2reader.load_replay("test_replays\\PVZ_ADEPT_BENCHMARK.SC2Replay")
rep_test = sc2reader.load_replay("test_replays\\PVZ_ADEPT_TESTCASE1.SC2Replay")
length_of_bench = rep_bench.frames // rep_bench.game_fps
length_of_test = rep_test.frames // rep_test.game_fps
min_game_length = min(length_of_bench, length_of_test)

#### WORKER TRACKING ####

wc_bench = worker_created(rep_bench, 1)
wc_test = worker_created(rep_test, 1)

wc_b_filter = filter_on_game_length(wc_bench, min_game_length)
wc_t_filter = filter_on_game_length(wc_test, min_game_length)

wc = unit_compare(wc_b_filter, wc_t_filter)

#sum up the deviation at each point that a worker is created
#w_dev = []
#w_sum = 0
#w_sum_abs = 0
#for x in range(len(wc)):
#    w_sum += wc[x]
#    w_sum_abs += abs(wc[x])
#    w_dev.append(w_sum)

#wc_roc = ROC(w_dev, len(w_dev))

#bo_w_dev_score = w_sum_abs / len(wc)

#this is different because wc_bench and wc_test might have the total workers from each replay, but the replays are different
#   lengths of time. 
#print("(why is this different?) BODw = {}s/w: Worker_total = {}".format(bo_w_dev_score, len(wc)))

#bod_w_100 = BOD(wc_bench, wc_test, 100)
#bod_w_200 = BOD(wc_bench, wc_test, 200)
#bod_w_300 = BOD(wc_bench, wc_test, 300)
#bod_w_400 = BOD(wc_bench, wc_test, 400)
#bod_w_500 = BOD(wc_bench, wc_test, 500)
bod_w_all = BOD(wc_bench, wc_test, min(length_of_bench, length_of_test))

#print("BODw@100 = {} s/w".format(bod_w_100))
#print("BODw@200 = {} s/w".format(bod_w_200))
#print("BODw@300 = {} s/w".format(bod_w_300))
#print("BODw@400 = {} s/w".format(bod_w_400))
#print("BODw@500 = {} s/w".format(bod_w_500))
print("BODw = {} s/w".format(bod_w_all))

final_dev_w = wc[len(wc)-1]

print("DEVw = {} s".format(final_dev_w))

# build order similarity score : 1 / (BOD / game_length) ==> 1 / ((w/s) / (s)) = w(orkers)
#print("BOSw@300 = {} w".format(1 / (bod_w_300 / 300)))
#print("BOSw@400 = {} w".format(1 / (bod_w_400 / 400)))
#print("BOSw@500 = {} w".format(1 / (bod_w_500 / min(500, length_of_bench, length_of_test))))


## Plotting
plt.figure()
plt.plot(wc, label='worker time deviations')
plt.xlabel('workers')
plt.ylabel('time (s)')
plt.legend()
plt.savefig('bin\\worker_time.svg')

#plt.figure()
#plt.plot(w_dev, label='worker deviation')
#plt.legend(loc=2)
#plt.savefig('bin\\worker_dev.svg')

#plt.figure()
#plt.plot(wc_roc, label='roc')
#plt.legend(loc=2)
#plt.savefig('bin\\worker_roc.svg')

#plt.figure()
#plt.plot(wc, label='worker time')
#plt.plot(w_dev, label='worker deviation')
#plt.plot(wc_roc, label='roc')
#plt.legend(loc=2)
#plt.savefig('bin\\worker_combined.svg')

plt.figure()
yb = []
for y in range(len(wc_b_filter)):
    yb.append(y)
plt.plot(wc_b_filter, yb, label='benchmark workers')

yp = []
for y in range(len(wc_t_filter)):
    yp.append(y)
plt.plot(wc_t_filter, yp, label='player workers')
plt.ylabel('workers')
plt.xlabel('time (s)')
plt.legend(loc=2)
plt.savefig('bin\\workers_created_comparison.svg')



#### ADEPT TRACKING ####

ac_bench = adept_created(rep_bench, 1)
ac_test = adept_created(rep_test, 1)

ac_b_filter = filter_on_game_length(ac_bench, min_game_length)
ac_t_filter = filter_on_game_length(ac_test, min_game_length)

ac = unit_compare(ac_b_filter, ac_t_filter)

#sum up the deviation at each point that an adept is created
#a_dev = []
#a_sum = 0
#a_sum_abs = 0
#for x in range(len(ac)):
#    a_sum += ac[x]
#    a_sum_abs += abs(ac[x])
#    a_dev.append(a_sum)

#ac_roc = ROC(ac, len(ac))
#ac_roc = ROC(a_dev, len(a_dev))

bod_a = BOD(ac_bench, ac_test, min(length_of_test, length_of_bench))
final_dev_a = ac[len(ac)-1]

print("BODa = {} s/a".format(bod_a))
print("DEVa = {} s".format(final_dev_a))


## Plotting
plt.figure()
plt.plot(ac, label='adept time deviations')
plt.xlabel('adepts')
plt.ylabel('time (s)')
plt.legend(loc=2)
plt.savefig('bin\\adept_time_deviations.svg')

#plt.figure()
#plt.plot(a_dev, label='adept deviation')
#plt.legend(loc=2)
#plt.savefig('bin\\adept_dev.svg')

#plt.figure()
#plt.plot(ac_roc, label='roc')
#plt.legend(loc=2)
#plt.savefig('bin\\adept_roc.svg')

#plt.figure()
#plt.plot(ac, label='adept time')
#plt.plot(a_dev, label='adept deviation')
#plt.plot(ac_roc, label='roc')
#plt.legend(loc=2)
#plt.savefig('bin\\adept_combined.svg')

plt.figure()
yb = []
for y in range(len(ac_b_filter)):
    yb.append(y)
plt.plot(ac_b_filter, yb, label='benchmark adepts')

yp = []
for y in range(len(ac_t_filter)):
    yp.append(y)
plt.plot(ac_t_filter, yp, label='player adepts')
plt.legend(loc=2)
plt.ylabel('adepts')
plt.xlabel('time (s)')
plt.savefig('bin\\adept_created_comparison.svg')



### BOD all ###
bod_all = (bod_w_all + bod_a) / 2

print("BOD = {} seconds / unit".format(bod_all))
