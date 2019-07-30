import random

from neural_network import NeuralNetwork
from ..metrics.bod import BuildOrderDeviation
from ..metrics.metric_factory.spawningtool_factory import SpawningtoolFactory
from ..metrics.metric_containers import *


bench_fact = SpawningtoolFactory('../tests/integration/test_replays/bod_tests/pvt_blink_robo_benchmark.SC2Replay')
bo_bench = bench_factory.generateBuildOrderElements('Gemini')
bod = BuildOrderDeviation(bo_bench)

rep_tuple = []
test_reps = '../tests/integration/test_replays'
for pth in os.listdir(test_paths):
    rep_tuple.append([os.path.join(test_reps, 'bod_tests', pth), 1])

rep_tuple.append([os.path.join(test_reps, 'pvz_macro.SC2Replay'), 0])
rep_tuple.append([os.path.join(test_reps, 'pvz_dt_archon_drop_executed_bo.SC2Replay'), 0])
rep_tuple.append([os.path.join(test_reps, 'pvz_dt_archon_drop_executed_bo_closer.SC2Replay'), 0])
rep_tuple.append([os.path.join(test_reps, 'pvz_dt_archon_drop_benchmark_bo.SC2Replay'), 0])

train_data = []
for tup in rep_tuple:
    fact = SpawningtoolFactory(tup[0])
    bo = fact.generateBuildOrderElements('NULL')
    if len(bo) > 0:
        bod.calculate_deviations(bo)
        train_data.append([bod.dev, bod.get_scaled_discrepency()], [tup[1]])
        print(bod.dev, ":", bod.get_scaled_discrepency(), ":", tup[1])


### Train
nn = NeuralNetwork(2, 1, 1)

for i in range(10000):
    tr_in, tr_out = random.choice(train_data)
    nn.train(tr_in, tr_out)

print("error: ", nn.calculate_total_error(train_data))



