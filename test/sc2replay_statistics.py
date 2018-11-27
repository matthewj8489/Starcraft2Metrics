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


def worker_compare(benchmark, player_workers, total):
    compare = []
    for x in range(total):
        compare.append(benchmark[x] - player_workers[x])

    return compare

def ROC(wp, total):
    roc = []
    x = 0
    while x < (total - 1):
        rocs = (wp[x+1] - wp[x])
        roc.append(rocs)
        x+=1

    return roc


rep_bench = sc2reader.load_replay("C:\\Users\\matthew\\Documents\\StarCraft II\\Accounts\\62997088\\1-S2-1-440880\\Replays\\Multiplayer\\PVZ_ADEPT_BENCHMARK.SC2Replay")
rep_test = sc2reader.load_replay("C:\\Users\\matthew\\Documents\\StarCraft II\\Accounts\\62997088\\1-S2-1-440880\\Replays\\Multiplayer\\PVZ_ADEPT_TESTCASE1.SC2Replay")

wc_bench = worker_created(rep_bench, 1)
wc_test = worker_created(rep_test, 1)

wc = worker_compare(wc_bench, wc_test, len(wc_bench))

wc_roc = ROC(wc, len(wc))

plt.figure()
plt.plot(wc, label='worker time')
plt.legend(loc=2)
plt.savefig('C:\\Users\\matthew\\Documents\\worker_time.svg')

plt.figure()
plt.plot(wc_roc, label='roc')
plt.legend(loc=2)
plt.savefig('C:\\Users\\matthew\\Documents\\roc.svg')

plt.figure()
plt.plot(wc, label='worker time')
plt.plot(wc_roc, label='roc')
plt.legend(loc=2)
plt.savefig('C:\\Users\\matthew\\Documents\\combined.svg')
