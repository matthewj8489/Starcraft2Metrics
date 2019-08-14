
def get_argument_parser():
    parser = argparse.ArgumentParser(description='Build Order Benchmark Comparison')

    parser.add_argument('benchmark_cache', type=str, help='The cache file containing benchmark build orders.')
    parser.add_argument('comparison_path', type=str, help='The build (.SC2Replay) or folder containing builds to compare to a benchmark build.')
    parser.add_argument('player_name', type=str, help='The name of the player to monitor in the comparison_build replay.')

    parser.add_argument('--add_to_cache', action='store_true', default=False, help='Add the comparison_build to the benchmark build cache instead of comparing it.')
    parser.add_argument('--add_to_cache_name', type=str, help='The name to store for the build order in cache. Default: race_vs_race_bo.')

    parser.add_argument('--latest', action='store_true', default=False, help='Use the latest build replay found in comparison_path. Used when comparison_path is a directory.')

    return parser


if __name__ == '__main__':
    import os
    import glob
    import argparse
    import json
    import csv
    import copy
    from metric_containers import *
    from build_order_detect import BuildOrderDetect
    from bod import BuildOrderDeviation
    from metric_factory.spawningtool_factory import SpawningtoolFactory
    from pprint import pprint

    parser = get_argument_parser()
    args = parser.parse_args()

    
    if not os.path.isdir(args.comparison_path) and not os.path.splitext(args.comparison_path)[1] == '.SC2Replay':#'.[Ss][Cc]2[Rr]eplay':
        print(os.path.splitext(args.comparison_path)[1])
        print('comparison_build requires .SC2Replay files to be used')
        raise SystemExit


    # load benchmark cache into memory as build orders
    bch_builds = []
    j_builds = []
    if os.path.isfile(args.benchmark_cache):
        with open(args.benchmark_cache, 'r') as bch_fl:
            j_builds = json.load(bch_fl)
            for j_bld in j_builds:
                bench_build = BuildOrder()
                bench_build.deserialize(copy.deepcopy(j_bld))
                bch_builds.append(bench_build)
            

    # gather each replay in the comparison_path
    replay_paths = []
    if os.path.isdir(args.comparison_path):
        if args.latest:
            replay_paths.append(max(glob.iglob(os.path.join(args.comparison_path, '*.[Ss][Cc]2[Rr]eplay')), key=os.path.getctime))
        else:
            for pth in os.listdir(args.comparison_path):
                if os.path.splitext(pth)[1] == '.SC2Replay':
                    replay_paths.append(os.path.join(args.comparison_path, pth))
    else:
        replay_paths.append(args.comparison_path)


    # cycle through each replay and add its analysis info
    for comp_pth in replay_paths:

        print(comp_pth)

        # load the comparison build order        
        cmp_bo_factory = SpawningtoolFactory(comp_pth)
        cmp_bo = cmp_bo_factory.generateBuildOrderElements(args.player_name)
        cmp_meta = cmp_bo_factory.generateReplayMetadata()

        # continue if the comparison build order has no build order elements (could be a replay without the specified player in it)
        if len(cmp_bo) == 0:
            print("Did not parse file as no build order for the specified player was found.")
            continue


        # If this build is being added to the build order cache, add it and exit
        if args.add_to_cache:
            bo = BuildOrder()
            bo.build = cmp_bo
            bo.name = args.add_to_cache_name
            j_builds.append(bo.serialize())
            with open(args.benchmark_cache, 'w') as bch_fl:
                json.dump(j_builds, bch_fl)
                print('Successfully added build to benchmark builds!')
                raise SystemExit


        # find the closest matching build order from the benchmarks
        closest_bod = None
        closest_confidence = 0
        closest_bch_name = ''
        for bch in bch_builds:
            confidence, bch_bod = BuildOrderDetect.detect_build_order(bch.build, cmp_bo)
            print(confidence, ":", bch.name)
            closest_bod = bch_bod if not closest_bod else closest_bod
            closest_bod = bch_bod if confidence >= closest_confidence else closest_bod
            closest_bch_name = bch.name if confidence >= closest_confidence else closest_bch_name
            closest_confidence = confidence if confidence >= closest_confidence else closest_confidence


        # report the build deviations
        out_path = 'bod_output.csv'
        out_file_exists = os.path.isfile(out_path)
        with open(out_path, 'a', newline='') as out_file:
            out_writer = csv.writer(out_file, quoting=csv.QUOTE_MINIMAL)
            if not out_file_exists:
                rw = ['deviation', 'scaled time dev', 'scaled order dev', 'depth', 'build', 'confidence'] + ReplayMetadata.csv_header()
                out_writer.writerow(rw)
            rw = [round(closest_bod.dev, 4), round(closest_bod.get_scaled_time_dev(), 4), round(closest_bod.get_scaled_order_dev(), 4), closest_bod.bench_depth, closest_bch_name, round(closest_confidence, 4)] + cmp_meta.to_csv_list()
            out_writer.writerow(rw)
            print('Successfully added the BOD metrics!')    

