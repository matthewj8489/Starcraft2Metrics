
def get_argument_parser():
    parser = argparse.ArgumentParser(description='Build Order Benchmark Comparison')

    parser.add_argument('benchmark_cache', type=str, help='The cache directory containing build orders.')
    parser.add_argument('comparison_build', type=str, help='The build (.SC2Replay) to compare to a benchmark build.')
    parser.add_argument('player_name', type=str, help='The name of the player to monitor in the comparison_build replay.')

    parser.add_argument('--add_to_cache', action='store_true', default=False, help='Add the comparison_build to the benchmark build cache instead of comparing it.')
    parser.add_argument('--add_to_cache_name', type=str, help='The name to store for the build order in cache. Default: race_vs_race_bo.')


if __name__ == '__main__':
    import os
    import argparse
    import json
    from metric_containers import *
    from build_order_detect import BuildOrderDetect

    parser = get_argument_parser()
    args = parser.parse_args()

            
    if not os.path.splitext(args.comparison_build)[1] == '.[Ss][Cc]2[Rr]eplay':
        print('comparison_build requires .SC2Replay files to be used')
        raise SystemExit


    # load benchmark cache into memory as build orders
    json_paths = []
    if os.path.isdir(args.benchmark_cache):
        for pth in os.listdir(args.benchmark_cache):
            if os.path.splitext(pth)[1] == '.json':
                json_paths.append(os.path.join(args.benchmark_cache, pth))

    bch_builds = []
    for j_pth in json_paths:
        with open(j_pth, 'r') as j_fl:
            bench_build = []
            j_bch = json.load(j_fl)
            for j_boe in j_bch:
                boe = BuildOrderElement
                boe.__dict__ = j_boe
                bench_build.append(boe)
            bch_build.append(bench_build)

    ###############
    # benchmark_cache is a json file containing all builds
    bch_builds = []
    with open(args.benchmark_cache) as bch_fl:
        j_builds = json.load(bch_fl)
        for j_bld in j_builds:
            bench_build = []
            for j_boe in j_bld:
                boe = BuildOrderElement
                boe.__dict__ = j_boe
                bench_build.append(j_boe)
            bch_builds.append(bench_build)

    ###############
    # using BuildOrder object instead...
    # benchmark_cache is a json file containing all builds
    bch_builds = []
    with open(args.benchmark_cache) as bch_fl:
        j_builds = json.load(bch_fl)
        for j_bld in j_builds:
            bench_build = BuildOrder
            bench_build.deserialize(j_bld)
            bch_builds.append(bench_build)
            
        
    cmp_bo_factory = SpawningtoolFactory(args.comparison_build)
    cmp_bo = cmp_bo_factory.generateBuildOrderElements(args.player_name)


    # If this build is being added to the build order cache, add it and exit
    if args.add_to_cache:
        

    if args.add_to_cache:
        bch_cache.append(cmp_bo.__dict__)
        with open(args.benchmark_cache, 'w') as bch_fl:
            json.dump(bch_fl, bch_cache)
            print('Successfully added build to benchmark builds!')
            raise SystemExit


        
    
