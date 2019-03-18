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


raw_filename = 'metrics.csv'
trend_filename = 'trends.csv'



def get_player_id(replay_file, player_name):
    replay = sc2reader.load_replay(replay_file)

    for player in replay.players:
        if player_name in player.name:
            return player.pid

    return -1


def matches_filter(rep_file, args):
    rep = sc2reader.load_replay(rep_file, load_level=2)

    #: Make sure that this replay is v2.0.8+, otherwise it won't be possible to pull useful data from it
    if rep.versions[1] < 2 or (rep.versions[1] == 2 and rep.versions[2] < 0) or (rep.versions[1] == 2 and rep.versions[2] == 0 and rep.versions[3] < 8):
        return False

    if args.ladder and not rep.is_ladder:
        return False

    if args.gametype and rep.game_type != args.gametype:
        return False

    return True


def get_replay_metadata(rep_file, player_id, args):
    meta = {'ReplayName' : '',
            'Date' : '',
            'Result' : '',
            'Map' : '',
            'RaceMatchup' : '',
            'GameLength' : 0,
            'GameType' : '',
            'IsLadder' : False,
            }

    if player_id >= 0:
        rep = sc2reader.load_replay(rep_file, load_level=2)

        matchup = ""
        for team in rep.teams:
            for player in team:
                matchup += player.pick_race[0]
            if team != rep.teams[len(rep.teams)-1]:
                matchup += "v"
        
        
        meta['ReplayName'] = os.path.basename(rep.filename)
        meta['Date'] = rep.start_time.strftime("%m/%d/%Y %H:%M:%S")
        meta['Result'] = rep.player[player_id].result
        meta['Map'] = rep.map_name
        meta['RaceMatchup'] = matchup
        meta['GameLength'] = rep.game_length.seconds
        meta['GameType'] = rep.game_type
        meta['IsLadder'] = rep.is_ladder

        return meta


def get_replay_raw_metrics(rep_file, player_id, args):
    return benchmark.Benchmark(rep_file, player_id).benchmarks()


def write_raw_output(outfilepath, metric_data, write_mode):
    with open(outfilepath, write_mode, newline='') as csvfile:
        if len(metric_data) > 0:
            writer = csv.DictWriter(csvfile, fieldnames=metric_data[0].keys())
            writer.writeheader()
            for rd in metric_data:
                writer.writerow(rd)
        

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
    parser.add_argument('player_name', type=str, help='The name of the player to gather the metric data on.')
    parser.add_argument('--recursive', action='store_true', default=True, help='Recursively read through the specified directory, searching for Starcraft II Replay files [default on]')
    parser.add_argument('--outpath', type=str, help='Specify the path for the output files. [default is same location as replay folder]')
    parser.add_argument('--gametype', type=str, help='Specify a game type to filter the replays upon.')
    parser.add_argument('--ladder-only', action='store_true', default=False, help='Filters out all replays that are not ladder games.')
    parser.add_argument('--overwrite', action='store_true', default=False, help='Overwrites output files when run. If not set, will append to any output files found.')
    parser.add_argument('--auto', action='store_true', default=False, help='Runs in the background and will automatically update output files when new replays appear.')
    args = parser.parse_args()
    
    replay_files = []
#    for root, dirs, files in os.walk(replays_directory):
#        for name in files:
#            replay_files.append(os.path.join(root, name))

    raw_filepath = ''
    if not args.outpath:
        raw_filepath = os.path.join(args.path, raw_filename)
    else:
        raw_filepath = os.path.join(args.outpath, raw_filename)
        

    for path in sc2reader.utils.get_files(args.path, extension='SC2Replay'):
        replay_files.append(path)

    raw_data = []
    for rep_file in replay_files:
        if (matches_filter(rep_file, args)):
            pid = get_player_id(rep_file, args.player_name)
            data = get_replay_metadata(rep_file, pid, args)
            data.update(get_replay_raw_metrics(rep_file, pid, args))
            raw_data.append(data)


    
