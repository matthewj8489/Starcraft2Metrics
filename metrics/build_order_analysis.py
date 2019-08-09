
def get_argument_parser():
    parser = argparse.ArgumentParser(description='Build Order Benchmark Comparison')

    parser.add_argument('benchmark_cache', type=str, help='The cache directory containing build orders.')
    parser.add_argument('comparison_build', type=str, help='The build (.SC2Replay) to compare to a benchmark build.')
    parser.add_argument('player_name', type=str, help='The name of the player to monitor in the comparison_build replay.')

    parser.add_argument('--add_to_cache', action='store_true', default=False, help='Add the comparison_build to the benchmark build cache instead of comparing it.')
    


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


    bch_builds = []
    with open(args.benchmark_cache, 'r'):
        bch_cache = json.load(args.benchmark_cache)
        for bch in bch_cache:
            boe = BuildOrderElement()
            boe.__dict__ = bch
            bch_builds.append(boe)

        
    cmp_bo_factory = SpawningtoolFactory(args.comparison_build)
    cmp_bo = cmp_bo_factory.generateBuildOrderElements(args.player_name)


    if args.add_to_cache:
        bch_cache.append(cmp_bo.__dict__)
        with open(args.benchmark_cache, 'w') as bch_fl:
            json.dump(bch_fl, bch_cache)
            print('Successfully added build to benchmark builds!')
            raise SystemExit


        
    
