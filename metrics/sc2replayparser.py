import sys
import os
import argparse
import sc2reader
import metrics
from sc2metric import Sc2MetricAnalyzer
import csv

##from plugins.supply import SupplyTracker
##from plugins.bases_created import BasesCreatedTracker
##from plugins.supply_created import SupplyCreatedTracker
##from plugins.resources import ResourceTracker
##from plugins.apm import APMTracker
##
##sc2reader.engine.register_plugin(SupplyTracker())
##sc2reader.engine.register_plugin(BasesCreatedTracker())
##sc2reader.engine.register_plugin(SupplyCreatedTracker())
##sc2reader.engine.register_plugin(ResourceTracker())
##sc2reader.engine.register_plugin(APMTracker())

#replays_directory = "C:\\Users\\matthew\\Documents\\StarCraft II\\Accounts\\62997088\\1-S2-1-440880\\Replays\\Multiplayer"
#replays_directory = "C:\\Users\\matthew\\Documents\\Starcraft2Metrics\\test\\test_replays"
#replays_directory = "C:\\Users\\matthew\\Documents\\gitprojects\\Starcraft2Metrics\\test\\test_replays"
#benchmark_data_file = "C:\\Users\\matthew\\Documents\\gitprojects\\Starcraft2Metrics\\test\\bin\\bench.csv"
#player_name = "NULL"


RAW_FILENAME = 'metrics.csv'
TREND_FILENAME = 'trends.csv'



def get_player_id(rep_lvl2, player_name):
    #replay = sc2reader.load_replay(replay_file, load_level=2)

    for player in rep_lvl2.players:
        if player_name in player.name:
            return player.pid

    return -1


def matches_filter(rep_lvl2, args):
    #rep = sc2reader.load_replay(rep_file, load_level=2)

    #: Make sure that this replay is v2.0.8+, otherwise it won't be possible to pull useful data from it
    if rep_lvl2.versions[1] < 2 or (rep_lvl2.versions[1] == 2 and rep_lvl2.versions[2] < 0) or (rep_lvl2.versions[1] == 2 and rep_lvl2.versions[2] == 0 and rep_lvl2.versions[3] < 8):
        return False

    if args.ladderonly and not rep_lvl2.is_ladder:
        return False

    if args.gametype and rep_lvl2.game_type != args.gametype:
        return False

    return True


def already_parsed(rep_file, parsed_files):
    for fl in parsed_files:
        if rep_file == fl:
            return True
    
    return False
    

def get_replay_metadata(rep_lvl2, player_id, args):
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
        #rep = sc2reader.load_replay(rep_file, load_level=2)

        matchup = ""
        for team in rep_lvl2.teams:
            for player in team:
                matchup += player.pick_race[0]
            if team != rep_lvl2.teams[len(rep_lvl2.teams)-1]:
                matchup += "v"
        
        
        meta['ReplayName'] = os.path.basename(rep_lvl2.filename)
        meta['Date'] = rep_lvl2.start_time.strftime("%m/%d/%Y %H:%M:%S")
        meta['Result'] = rep_lvl2.player[player_id].result
        meta['Map'] = rep_lvl2.map_name
        meta['RaceMatchup'] = matchup
        meta['GameLength'] = rep_lvl2.game_length.seconds
        meta['GameType'] = rep_lvl2.game_type
        meta['IsLadder'] = rep_lvl2.is_ladder

        return meta


def get_replay_raw_metrics(player_metrics):
    return player_metrics.metrics()


def write_raw_output(outfilepath, metric_data, write_mode):
    with open(outfilepath, write_mode, newline='') as csvfile:
        if len(metric_data) > 0:
            writer = csv.DictWriter(csvfile, fieldnames=metric_data[0].keys())
            # write the header if this is a new file (not appended file)
            if write_mode == 'w+':
                writer.writeheader()
            for rd in metric_data:
                writer.writerow(rd)
        

##def get_replay_data(replay_files, args):
##    replay_data = []
##    for rep in replay_files:       
##        data_dict = {'ReplayName' : '',
##                     'Date' : '',
##                     'Result' : '',
##                     'Map' : '',
##                     'RaceMatchup' : '',
##                     'GameLength' : 0,
##                     'GameType' : '',
##                     'IsLadder' : False,
##                    }
##        player_id = get_player_id(rep, player_name)
##        if player_id >= 0:
##            rep_obj = sc2reader.load_replay(rep, load_level=2)
##
##            #: Make sure that this replay is v2.0.8+, otherwise it won't be possible to pull useful data from it
##            if rep_obj.versions[1] < 2 or (rep_obj.versions[1] == 2 and rep_obj.versions[2] < 0) or (rep_obj.versions[1] == 2 and rep_obj.versions[2] == 0 and rep_obj.versions[3] < 8):
##                continue
##
##            if args.ladder and not rep_obj.is_ladder:
##                continue
##
##            if args.gametype and rep_obj.game_type != args.gametype:
##                continue          
##
##            
##            matchup = ""
##            for team in rep_obj.teams:
##                for player in team:
##                    matchup += player.pick_race[0]
##                if team != rep_obj.teams[len(rep_obj.teams)-1]:
##                    matchup += "v"
##            
##            
##            data_dict['ReplayName'] = os.path.basename(rep_obj.filename)
##            data_dict['Date'] = rep_obj.start_time.strftime("%m/%d/%Y %H:%M:%S")
##            data_dict['Result'] = rep_obj.player[player_id].result
##            data_dict['Map'] = rep_obj.map_name
##            data_dict['RaceMatchup'] = matchup
##            data_dict['GameLength'] = rep_obj.game_length.seconds
##            data_dict['GameType'] = rep_obj.game_type
##            data_dict['IsLadder'] = rep_obj.is_ladder
##            bc = benchmark.Benchmark(rep, player_id)
##            data_dict.update(bc.benchmarks())
##
##            replay_data.append(data_dict)
##
##    return replay_data


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
    replay_files = []
    write_mode = ''
    raw_filepath = ''
    raw_data = []
    parsed_rep_filenames = []
    
    parser = argparse.ArgumentParser(description='Parse benchmarks from a set of replays')

    parser.add_argument('path', type=str, help='The folder path containing the replays to be parsed')
    parser.add_argument('player_name', type=str, help='The name of the player to gather the metric data on.')
    parser.add_argument('--recursive', action='store_true', default=True, help='Recursively read through the specified directory, searching for Starcraft II Replay files [default on]')
    parser.add_argument('--outpath', type=str, help='Specify the path for the output files. [default is same location as replay folder]')
    parser.add_argument('--gametype', type=str, help='Specify a game type to filter the replays upon.')
    parser.add_argument('--ladderonly', action='store_true', default=False, help='Filters out all replays that are not ladder games.')
    parser.add_argument('--overwrite', action='store_true', default=False, help='Overwrites output files when run. If not set, will append to any output files found.')
    parser.add_argument('--auto', action='store_true', default=False, help='Runs in the background and will automatically update output files when new replays appear.')
    args = parser.parse_args()
    

#    for root, dirs, files in os.walk(replays_directory):
#        for name in files:
#            replay_files.append(os.path.join(root, name))

    # Handle the arguments
    if not args.outpath:
        raw_filepath = os.path.join(args.path, RAW_FILENAME)
    else:
        raw_filepath = os.path.join(args.outpath, RAW_FILENAME)

    # create any necessary directories
    if not os.path.exists(os.path.dirname(raw_filepath)):
        try:
            os.makedirs(os.path.dirname(raw_filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if args.overwrite:
        write_mode = 'w+'
    else:
        if os.path.isfile(raw_filepath):
            write_mode = 'a'
            with open(raw_filepath, newline='') as csvfile:
                rep_rdr = csv.DictReader(csvfile)
                for row in rep_rdr:
                    parsed_rep_filenames.append(row['ReplayName'])
        else:
            write_mode = 'w+'

        
    # Find all possible replay files
    for path in sc2reader.utils.get_files(args.path, extension='SC2Replay'):
        replay_files.append(path)


    # parse replay files
    for rep_file in replay_files:
        if (not already_parsed(os.path.basename(rep_file), parsed_rep_filenames)):
            rep_lvl2 = sc2reader.load_replay(rep_file, load_level=2)
            if (matches_filter(rep_lvl2, args)):
                pid = get_player_id(rep_lvl2, args.player_name)
                data = get_replay_metadata(rep_lvl2, pid, args)
                rep_all = sc2reader.load_replay(rep_file)
                data.update(get_replay_raw_metrics(rep_all.player[pid].metrics))
                raw_data.append(data)


    # write the raw output file
    write_raw_output(raw_filepath, raw_data, write_mode)
    
