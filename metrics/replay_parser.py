import sys
import os
import sc2reader
import benchmark

#replays_directory = "C:\\Users\\matthew\\Documents\\StarCraft II\\Accounts\\62997088\\1-S2-1-440880\\Replays\\Multiplayer"
#replays_directory = "C:\\Users\\matthew\\Documents\\Starcraft2Metrics\\test\\test_replays"
replays_directory = "C:\\Users\\matthew\\Documents\\Starcraft2Metrics\\test\\temp"
player_name = "NULL"
benchmark_time_s = 720

def get_player_id(replay_file, player_name):
    replay = sc2reader.load_replay(replay_file)

    for player in replay.players:
        if player_name in player.name:
            return player.pid

    return -1


replay_files = []
for root, dirs, files in os.walk(replays_directory):
    for name in files:
        replay_files.append(os.path.join(root, name))

benchmarks = []
for rep in replay_files:
    player_id = get_player_id(rep, player_name)
    if player_id >= 0:
        benchmarks.append(benchmark.benchmark(rep, player_id, benchmark_time_s))

for bench in benchmarks:
    if bench['BenchmarkLength'] == benchmark_time_s:
        print(bench)
                                 
