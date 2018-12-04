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


def worker_compare(benchmark, player_workers):
    compare = []
    total = min(len(benchmark), len(player_workers))
    for x in range(total):
        compare.append(benchmark[x] - player_workers[x])

    return compare


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

    return army


def ROC(wp, total):
    roc = []
    x = 0
    while x < (total - 1):
        rocs = (wp[x+1] - wp[x])
        roc.append(rocs)
        x+=1

    return roc


rep_bench = sc2reader.load_replay("test_replays\\PVZ_ADEPT_BENCHMARK.SC2Replay")
rep_test = sc2reader.load_replay("test_replays\\PVZ_ADEPT_TESTCASE1.SC2Replay")

#### WORKER TRACKING ####

wc_bench = worker_created(rep_bench, 1)
wc_test = worker_created(rep_test, 1)

wc = worker_compare(wc_bench, wc_test)

#sum up the deviation at each point that a worker is created
w_dev = []
w_sum = 0
for x in range(len(wc)):
    w_sum += wc[x]
    w_dev.append(w_sum)

#wc_roc = ROC(wc, len(wc))
wc_roc = ROC(w_dev, len(w_dev))

plt.figure()
plt.plot(wc, label='worker time')
plt.legend(loc=2)
plt.savefig('bin\\worker_time.svg')

plt.figure()
plt.plot(w_dev, label='worker deviation')
plt.legend(loc=2)
plt.savefig('bin\\worker_dev.svg')

plt.figure()
plt.plot(wc_roc, label='roc')
plt.legend(loc=2)
plt.savefig('bin\\worker_roc.svg')

plt.figure()
plt.plot(wc, label='worker time')
plt.plot(w_dev, label='worker deviation')
plt.plot(wc_roc, label='roc')
plt.legend(loc=2)
plt.savefig('bin\\worker_combined.svg')

plt.figure()
yb = []
for y in range(len(wc_bench)):
    yb.append(y)
plt.plot(wc_bench, yb, label='benchmark workers')

yp = []
for y in range(len(wc_test)):
    yp.append(y)
plt.plot(wc_test, yp, label='player workers')
plt.legend(loc=2)
plt.savefig('bin\\worker_created.svg')


#### ADEPT TRACKING ####

ac_bench = adept_created(rep_bench, 1)
ac_test = adept_created(rep_test, 1)

ac = worker_compare(ac_bench, ac_test)

#sum up the deviation at each point that an adept is created
a_dev = []
a_sum = 0
for x in range(len(ac)):
    a_sum += ac[x]
    a_dev.append(a_sum)

#ac_roc = ROC(ac, len(ac))
ac_roc = ROC(a_dev, len(a_dev))

plt.figure()
plt.plot(ac, label='adept time')
plt.legend(loc=2)
plt.savefig('bin\\adept_time.svg')

plt.figure()
plt.plot(a_dev, label='adept deviation')
plt.legend(loc=2)
plt.savefig('bin\\adept_dev.svg')

plt.figure()
plt.plot(ac_roc, label='roc')
plt.legend(loc=2)
plt.savefig('bin\\adept_roc.svg')

plt.figure()
plt.plot(ac, label='adept time')
plt.plot(a_dev, label='adept deviation')
plt.plot(ac_roc, label='roc')
plt.legend(loc=2)
plt.savefig('bin\\adept_combined.svg')

plt.figure()
yb = []
for y in range(len(ac_bench)):
    yb.append(y)
plt.plot(ac_bench, yb, label='benchmark adepts')

yp = []
for y in range(len(ac_test)):
    yp.append(y)
plt.plot(ac_test, yp, label='player adepts')
plt.legend(loc=2)
plt.savefig('bin\\adept_created.svg')

