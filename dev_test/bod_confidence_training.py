import os
import random

from neural_network import NeuralNetwork
from bod import BuildOrderDeviation
from metric_factory.spawningtool_factory import SpawningtoolFactory
from metric_containers import *


bench_fact = SpawningtoolFactory('../tests/integration/test_replays/bod_tests/pvt_blink_robo_benchmark.SC2Replay')
bo_bench = bench_fact.generateBuildOrderElements('Gemini')
bod_blink_robo = BuildOrderDeviation(bo_bench)

bench_fact = SpawningtoolFactory('../tests/integration/test_replays/bod_tests/pvp_2_gate_expand_benchmark_Gemini.SC2Replay')
bo_bench = bench_fact.generateBuildOrderElements('Gemini')
bod_2_gate_expand = BuildOrderDeviation(bo_bench)

bench_fact = SpawningtoolFactory('../tests/integration/test_replays/bod_tests/pvz_dt_archon_drop_benchmark_Gemini.SC2Replay')
bo_bench = bench_fact.generateBuildOrderElements('Gemini')
bod_dt_archon_drop = BuildOrderDeviation(bo_bench)

bench_fact = SpawningtoolFactory('../tests/integration/test_replays/bod_tests/pvz_chargelot_allin_NULL.SC2Replay')
bo_bench = bench_fact.generateBuildOrderElements('NULL')
bod_dt_archon_drop = BuildOrderDeviation(bo_bench)


rep_tuples = {'blink_robo': [], '2_gate_expand': [], 'dt_archon_drop': [], 'chargelot_allin': []}
test_reps = '../tests/integration/test_replays/bod_tests/'
for pth in os.listdir(os.path.join(test_reps, 'pvt_blink_robo/')):
    rep_tuples['blink_robo'].append([os.path.join(test_reps, 'pvt_blink_robo/', pth), 1])
    rep_tuples['2_gate_expand'].append([os.path.join(test_reps, 'pvt_blink_robo/', pth), 0])
    rep_tuples['dt_archon_drop'].append([os.path.join(test_reps, 'pvt_blink_robo/', pth), 0])
    rep_tuples['chargelot_allin'].append([os.path.join(test_reps, 'pvt_blink_robo/', pth), 0])

for pth in os.listdir(os.path.join(test_reps, 'pvp_2_gate_expand/')):
    rep_tuples['blink_robo'].append([os.path.join(test_reps, 'pvp_2_gate_expand/', pth), 0])
    rep_tuples['2_gate_expand'].append([os.path.join(test_reps, 'pvp_2_gate_expand/', pth), 1])
    rep_tuples['dt_archon_drop'].append([os.path.join(test_reps, 'pvp_2_gate_expand/', pth), 0])
    rep_tuples['chargelot_allin'].append([os.path.join(test_reps, 'pvp_2_gate_expand/', pth), 0])

for pth in os.listdir(os.path.join(test_reps, 'pvz_dt_archon_drop/')):
    rep_tuples['blink_robo'].append([os.path.join(test_reps, 'pvz_dt_archon_drop/', pth), 0])
    rep_tuples['2_gate_expand'].append([os.path.join(test_reps, 'pvz_dt_archon_drop/', pth), 0])
    rep_tuples['dt_archon_drop'].append([os.path.join(test_reps, 'pvz_dt_archon_drop/', pth), 1])
    rep_tuples['chargelot_allin'].append([os.path.join(test_reps, 'pvz_dt_archon_drop/', pth), 0])

train_data = []
for tup in rep_tuples['blink_robo']:
    fact = SpawningtoolFactory(tup[0])
    bo = fact.generateBuildOrderElements('NULL')
    bod = bod_blink_robo
    if len(bo) > 0:
        bod.calculate_deviations(bo)
        train_data.append([[bod.get_scaled_order_dev(), bod.get_scaled_discrepency()], [tup[1]]])
        print(bod.dev, ":", bod.get_scaled_discrepency(), ":", tup[1], ":", tup[0])

for tup in rep_tuples['2_gate_expand']:
    fact = SpawningtoolFactory(tup[0])
    bo = fact.generateBuildOrderElements('NULL')
    bod = bod_2_gate_expand
    if len(bo) > 0:
        bod.calculate_deviations(bo)
        train_data.append([[bod.get_scaled_order_dev(), bod.get_scaled_discrepency()], [tup[1]]])
        print(bod.dev, ":", bod.get_scaled_discrepency(), ":", tup[1], ":", tup[0])

for tup in rep_tuples['dt_archon_drop']:
    fact = SpawningtoolFactory(tup[0])
    bo = fact.generateBuildOrderElements('NULL')
    bod = bod_dt_archon_drop
    if len(bo) > 0:
        bod.calculate_deviations(bo)
        train_data.append([[bod.get_scaled_order_dev(), bod.get_scaled_discrepency()], [tup[1]]])
        print(bod.dev, ":", bod.get_scaled_discrepency(), ":", tup[1], ":", tup[0])

for tup in rep_tuples['chargelot_allin']:
    fact = SpawningtoolFactory(tup[0])
    bo = fact.generateBuildOrderElements('NULL')
    bod = bod_dt_archon_drop
    if len(bo) > 0:
        bod.calculate_deviations(bo)
        train_data.append([[bod.get_scaled_order_dev(), bod.get_scaled_discrepency()], [tup[1]]])
        print(bod.dev, ":", bod.get_scaled_discrepency(), ":", tup[1], ":", tup[0])

### Train
nn = NeuralNetwork(2, 2, 1)

for i in range(100000):
    tr_in, tr_out = random.choice(train_data)
    nn.train(tr_in, tr_out)

for dt in train_data:
    print(dt[0], dt[1], nn.feed_forward(dt[0]))

print("error: ", nn.calculate_total_error(train_data))



