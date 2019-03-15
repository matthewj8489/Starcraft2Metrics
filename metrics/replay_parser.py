import sys
import os
import argparse
import sc2reader
import benchmark
import csv

#replays_directory = "C:\\Users\\matthew\\Documents\\StarCraft II\\Accounts\\62997088\\1-S2-1-440880\\Replays\\Multiplayer"
#replays_directory = "C:\\Users\\matthew\\Documents\\Starcraft2Metrics\\test\\test_replays"
replays_directory = "C:\\Users\\matthew\\Documents\\gitprojects\\Starcraft2Metrics\\test\\test_replays"
benchmark_data_file = "C:\\Users\\matthew\\Documents\\gitprojects\\Starcraft2Metrics\\test\\bin\\bench.csv"
player_name = "NULL"


def get_player_id(replay_file, player_name):
    replay = sc2reader.load_replay(replay_file)

    for player in replay.players:
        if player_name in player.name:
            return player.pid

    return -1


#: {ReplayName, RaceMatchup, GameLength, GameType, IsLadder, Benchmark.benchmarks}
def get_replay_data(replay_files, args):
    replay_data = []
    for rep in replay_files:       
        data_dict = {'ReplayName' : '',
                     'Date' : '',
                     'Result' : '',
                     'Map' : '',
                     'RaceMatchup' : '',
                     'GameLength' : 0,
                     'GameType' : '',
                     'IsLadder' : False,
                    }
        player_id = get_player_id(rep, player_name)
        if player_id >= 0:
            rep_obj = sc2reader.load_replay(rep, load_level=2)

            #: Make sure that this replay is v2.0.8+, otherwise it won't be possible to pull useful data from it
            if rep_obj.versions[1] < 2 or (rep_obj.versions[1] == 2 and rep_obj.versions[2] < 0) or (rep_obj.versions[1] == 2 and rep_obj.versions[2] == 0 and rep_obj.versions[3] < 8):
                continue

            if args.ladder and not rep_obj.is_ladder:
                continue

            if args.gametype and rep_obj.game_type != args.gametype:
                continue          

            
            matchup = ""
            for team in rep_obj.teams:
                for player in team:
                    matchup += player.pick_race[0]
                if team != rep_obj.teams[len(rep_obj.teams)-1]:
                    matchup += "v"
            
            
            data_dict['ReplayName'] = os.path.basename(rep_obj.filename)
            data_dict['Date'] = rep_obj.start_time.strftime("%m/%d/%Y %H:%M:%S")
            data_dict['Result'] = rep_obj.player[player_id].result
            data_dict['Map'] = rep_obj.map_name
            data_dict['RaceMatchup'] = matchup
            data_dict['GameLength'] = rep_obj.game_length.seconds
            data_dict['GameType'] = rep_obj.game_type
            data_dict['IsLadder'] = rep_obj.is_ladder
            bc = benchmark.Benchmark(rep, player_id)
            data_dict.update(bc.benchmarks())

            replay_data.append(data_dict)

    return replay_data


def multi_replay_analysis(bench_data):
    # metric[0] = best
    # metric[1] = avg 30 games

    metric_dict = {metric: {'Best' : 0, 'Avg30Games' : 0} for metric in bench_data.keys}

    ttm_filter = list(filter(lambda ttm: ttm >= 0, bench_data['TimeToMax']))
    metric_dict['TimeToMax']['Best'] = min(ttm_filter)
    ttm_avg_idx = min(len(ttm_filter) - 1, 29)
    ttm_sum = 0
    for idx in range(len(ttm_filter) - 1 - ttm_avg_idx, len(ttm_filter) - 1, 1):
        ttm_sum += ttm_filter[idx]
    ttm_avg = ttm_sum / (ttm_avg_idx + 1)
    metric_dict['TimeToMax']['Avg30Games'] = ttm_avg
                   


############ MAIN ##############
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse benchmarks from a set of replays')

    parser.add_argument('path', type=str, help='The folder path containing the replays to be parsed')
    parser.add_argument('--recursive', action='store_true', default=True, help='Recursively read through the specified directory, searching for Starcraft II Replay files [default on]')
    parser.add_argument('--outfile', type=str, help='Specify the filepath for the output .csv file filled with benchmark data. [default is same location as replay folder]')
    parser.add_argument('--gametype', type=str, help='Specify a game type to filter the replays upon.')
    parser.add_argument('--ladder', action='store_true', default=False, help='Filters out all replays that are not ladder games.')
    arguments = parser.parse_args()
    
    replay_files = []
#    for root, dirs, files in os.walk(replays_directory):
#        for name in files:
#            replay_files.append(os.path.join(root, name))

    data_file = ''
    if not arguments.outfile:
        data_file = os.path.join(arguments.path, "bench.csv")
    else:
        data_file = arguments.outfile
        

    for path in sc2reader.utils.get_files(arguments.path, extension='SC2Replay'):
        replay_files.append(path)

    with open(data_file, 'w', newline='') as csvfile:
        rep_data = get_replay_data(replay_files, arguments)
        if len(rep_data) > 0:
            writer = csv.DictWriter(csvfile, fieldnames=rep_data[0].keys())
            writer.writeheader()
            for rd in rep_data:
                writer.writerow(rd)
