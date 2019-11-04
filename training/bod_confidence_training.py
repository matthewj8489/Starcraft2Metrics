import os
import sys
import random
import json

if __name__ == '__main__':
    sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import metrics
from metrics.neural_network import NeuralNetwork    
from metrics.bod import BuildOrderDeviation
from metrics.metric_factory.spawningtool_factory import SpawningtoolFactory
from metrics.metric_containers import *
import metrics.unit_constants as uc

bench_fact = SpawningtoolFactory('build_order_detect_training_test_replays/pvt_blink_robo_benchmark.SC2Replay')
bo_bench = bench_fact.generateBuildOrderElements('Gemini')
bod_blink_robo = BuildOrderDeviation(bo_bench)

bench_fact = SpawningtoolFactory('build_order_detect_training_test_replays/pvp_2_gate_expand_benchmark_Gemini.SC2Replay')
bo_bench = bench_fact.generateBuildOrderElements('Gemini')
bod_2_gate_expand = BuildOrderDeviation(bo_bench)

bench_fact = SpawningtoolFactory('build_order_detect_training_test_replays/pvz_dt_archon_drop_benchmark_Gemini.SC2Replay')
bo_bench = bench_fact.generateBuildOrderElements('Gemini')
bod_dt_archon_drop = BuildOrderDeviation(bo_bench)

bench_fact = SpawningtoolFactory('build_order_detect_training_test_replays/pvz_chargelot_allin_benchmark_NULL.SC2Replay')
bo_bench = bench_fact.generateBuildOrderElements('NULL')
bod_chargelot_allin = BuildOrderDeviation(bo_bench)

bench_fact = SpawningtoolFactory('build_order_detect_training_test_replays/pvz_sentry_drop_into_soul_train_benchmark_Gemini.SC2Replay')
bo_bench = bench_fact.generateBuildOrderElements('Gemini')
bod_sentry_drop_soul_train = BuildOrderDeviation(bo_bench)

# create tuples for each build order over all the test replays from each build
rep_tuples = {'blink_robo': [], '2_gate_expand': [], 'dt_archon_drop': [], 'chargelot_allin': [], 'sentry_drop_soul_train': []}
test_reps = 'build_order_detect_training_test_replays/'

blink_robo_path = os.path.join(test_reps, 'pvt_blink_robo/')
for pth in os.listdir(blink_robo_path):
    rep_path = os.path.join(blink_robo_path, pth)
    if os.path.splitext(pth)[1] == '.SC2Replay':
        rep_tuples['blink_robo'].append([rep_path, 1])
        rep_tuples['2_gate_expand'].append([rep_path, 0])
        rep_tuples['dt_archon_drop'].append([rep_path, 0])
        rep_tuples['chargelot_allin'].append([rep_path, 0])
        rep_tuples['sentry_drop_soul_train'].append([rep_path, 0])

_2_gate_expand_path = os.path.join(test_reps, 'pvp_2_gate_expand/')
for pth in os.listdir(_2_gate_expand_path):
    rep_path = os.path.join(_2_gate_expand_path, pth)
    if os.path.splitext(pth)[1] == '.SC2Replay':
        rep_tuples['blink_robo'].append([rep_path, 0])
        rep_tuples['2_gate_expand'].append([rep_path, 1])
        rep_tuples['dt_archon_drop'].append([rep_path, 0])
        rep_tuples['chargelot_allin'].append([rep_path, 0])
        rep_tuples['sentry_drop_soul_train'].append([rep_path, 0])

dt_archon_drop_path = os.path.join(test_reps, 'pvz_dt_archon_drop/')
for pth in os.listdir(dt_archon_drop_path):
    rep_path = os.path.join(dt_archon_drop_path, pth)
    if os.path.splitext(pth)[1] == '.SC2Replay':
        rep_tuples['blink_robo'].append([rep_path, 0])
        rep_tuples['2_gate_expand'].append([rep_path, 0])
        rep_tuples['dt_archon_drop'].append([rep_path, 1])
        rep_tuples['chargelot_allin'].append([rep_path, 0])
        rep_tuples['sentry_drop_soul_train'].append([rep_path, 0])

chargelot_allin_path = os.path.join(test_reps, 'pvz_chargelot_allin/')
for pth in os.listdir(chargelot_allin_path):
    rep_path = os.path.join(chargelot_allin_path, pth)
    if os.path.splitext(pth)[1] == '.SC2Replay':
        rep_tuples['blink_robo'].append([rep_path, 0])
        rep_tuples['2_gate_expand'].append([rep_path, 0])
        rep_tuples['dt_archon_drop'].append([rep_path, 0])
        rep_tuples['chargelot_allin'].append([rep_path, 1])
        rep_tuples['sentry_drop_soul_train'].append([rep_path, 0])

unknown_path = os.path.join(test_reps, 'unknown/')
for pth in os.listdir(unknown_path):
    rep_path = os.path.join(unknown_path, pth)
    if os.path.splitext(pth)[1] == '.SC2Replay':
        rep_tuples['blink_robo'].append([rep_path, 0])
        rep_tuples['2_gate_expand'].append([rep_path, 0])
        rep_tuples['dt_archon_drop'].append([rep_path, 0])
        rep_tuples['chargelot_allin'].append([rep_path, 0])
        rep_tuples['sentry_drop_soul_train'].append([rep_path, 0])


# find the bod metrics for each replay tuple and add them to the train_data
train_data = []

def get_additional_train_data(td_path, rep_tuple, bod_bench):
    train_data_tmp = []
    if os.path.isfile(td_path):
        with open(td_path, 'r') as td_fl:
            train_data_tmp = json.load(td_fl)
    else:
        for tup in rep_tuple:
            fact = SpawningtoolFactory(tup[0])
            bo = fact.generateBuildOrderElements('NULL')
            bod = bod_bench
            if len(bo) > 0:
                bod.calculate_deviations(bo)
                #train_data_tmp.append([[bod.get_scaled_order_dev(), bod.get_scaled_discrepency()], [tup[1]]])
                train_data_tmp.append([[bod.get_scaled_order_dev(),
                                        bod.get_scaled_tag_order_dev(uc.WORKER_TAG),
                                        bod.get_scaled_tag_order_dev(uc.ARMY_TAG),
                                        bod.get_scaled_tag_order_dev(uc.BUILDING_TAG),
                                        bod.get_scaled_tag_order_dev(uc.UPGRADE_TAG),
                                        bod.get_scaled_tag_order_dev(uc.BASE_TAG),
                                        bod.get_scaled_tag_order_dev(uc.SUPPLY_TAG),
                                        bod.get_scaled_tag_order_dev(uc.PRODUCTION_TAG),
                                        bod.get_scaled_tag_order_dev(uc.TECH_TAG),
                                        bod.get_scaled_tag_order_dev(uc.STAT_TAG),
                                        bod.get_scaled_discrepency()], [tup[1]]])
                print(bod.dev, ":", bod.get_scaled_discrepency(), ":", tup[1], ":", tup[0])
        
        with open(td_path, 'w') as td_fl:
            json.dump(train_data_tmp, td_fl)

    return train_data_tmp


train_data += get_additional_train_data(os.path.join(test_reps, 'pvt_blink_robo/', 'train_data.json'), rep_tuples['blink_robo'], bod_blink_robo)

train_data += get_additional_train_data(os.path.join(test_reps, 'pvp_2_gate_expand/', 'train_data.json'), rep_tuples['2_gate_expand'], bod_2_gate_expand)

train_data += get_additional_train_data(os.path.join(test_reps, 'pvz_dt_archon_drop/', 'train_data.json'), rep_tuples['dt_archon_drop'], bod_dt_archon_drop)

train_data += get_additional_train_data(os.path.join(test_reps, 'pvz_chargelot_allin/', 'train_data.json'), rep_tuples['chargelot_allin'], bod_chargelot_allin)

train_data += get_additional_train_data(os.path.join(test_reps, 'pvz_sentry_drop_soul_train/', 'train_data.json'), rep_tuples['sentry_drop_soul_train'], bod_sentry_drop_soul_train)


### Train
#nn = NeuralNetwork(2, 3, 1)
nn = NeuralNetwork(11, 4, 1)

for i in range(500000):
    tr_in, tr_out = random.choice(train_data)
    nn.train(tr_in, tr_out)

for dt in train_data:
    print(dt[0], dt[1], nn.feed_forward(dt[0]))

print("error: ", nn.calculate_total_error(train_data))



