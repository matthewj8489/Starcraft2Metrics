import sys
import os
import argparse
import sc2reader
import benchmark
import csv

#replays_directory = "C:\\Users\\matthew\\Documents\\StarCraft II\\Accounts\\62997088\\1-S2-1-440880\\Replays\\Multiplayer"
#replays_directory = "C:\\Users\\matthew\\Documents\\Starcraft2Metrics\\test\\test_replays"
replays_directory = "C:\\Users\\matthew\\Documents\\Starcraft2Metrics\\test\\temp"
benchmark_data_file = "C:\\Users\\matthew\\Documents\\SC2Benchmarks\\benchmarks.csv"
player_name = "NULL"


def get_player_id(replay_file, player_name):
    replay = sc2reader.load_replay(replay_file)

    for player in replay.players:
        if player_name in player.name:
            return player.pid

    return -1


#: {ReplayName, RaceMatchup, GameLength, GameType, IsLadder, Benchmark.benchmarks}
def get_replay_data(replay_files):
    replay_data = []
    for rep in replay_files:
        data_dict = {'ReplayName' : '',
                     'Date' : '',                     
                     'Map' : '',
                     'RaceMatchup' : '',
                     'GameLength' : 0,
                     'GameType' : '',
                     'IsLadder' : False,
                    }
        player_id = get_player_id(rep, player_name)
        if player_id >= 0:
            rep_obj = sc2reader.load_replay(rep, load_level=2)
            matchup = ""
            for team in replay.teams:
                for player in team:
                    matchup += player.pick_race[0]
                matchup += "v"
            
            data_dict['ReplayName'] = rep_obj.filename
            data_dict['Date'] = rep_obj.start_time.strftime("%Y-%m-%d %H:%M:%s")
            data_dict['Map'] = rep_obj.map_name
            data_dict['RaceMatchup'] = matchup
            data_dict['GameLength'] = rep_obj.game_length.seconds
            data_dict['GameType'] = rep_obj.game_type
            data_dict['IsLadder'] = rep_obj.is_ladder
            bc = benchmark.Benchmark(rep)
            data_dict.update(bc.benchmarks)

            replay_data.append(data_dict)

    return replay_data


############ MAIN ##############
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse benchmarks from a set of replays')

    parser.add_argument('path', type=str, help='The folder path containing the replays to be parsed')
    parser.add_argument('--recursive', action='store_true', default=True, help='Recursively read through the specified directory, searching for Starcraft II Replay files [default on]')
    parser.add_argument('--outfile', type=str, help='Specify the filepath for the output .csv file filled with benchmark data. [default is same location as replay folder]')
    arguments = parser.parse_args()
    
    replay_files = []
#    for root, dirs, files in os.walk(replays_directory):
#        for name in files:
#            replay_files.append(os.path.join(root, name))

    for path in sc2reader.utils.get_files(arguments.path, extension='SC2Replay'):
        replay_files.append(path)

    with open(benchmark_data_file, 'w') as csvfile:
        rep_data = get_replay_data(replay_files)
        if len(rep_data) > 0:
            writer = csv.DictWriter(csvfile, fieldnames=rep_data[0].keys())
            for rd in rep_data:
                writer.writerow(rd)
