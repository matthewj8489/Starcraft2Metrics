import itertools
import math
from metrics.unit_constants import get_tags

# Outputs:
# dev - a metric that averages the scaled values of time deviation and
#       order deviation to give an overall value of closeness to the
#       benchmark build order. A zero means the builds are exactly
#       the same.
# time_dev      - total deviation in time (absolute values?)
# time_dev_p    - additional time_dev accounting for missing build items
# order_dev     - total deviation in order (absolute values?)
# order_dev_p   - additional order_dev accounting for missing build items
# discrepency   - total discrepencies in build (elements missing or elements
#               that shouldn't be there)
# acc_time_dev  - the accumulated deviation in time vs bench build ordering
# acc_order_dev - the accumulated deviation in order vs bench build ordering
# dev_arr   - array containing the benchmark, build, dev_supp, dev_time for
#           each build order element
#           Bench((order)[time]supp|unit),Build,dev_supp,dev_time
#           (1)[0:00]12|Probe,(1)[0:00]12|Probe,0,0:00
#           (2)[0:13]13|Probe,(2)[0:14]13|Probe,0,+0:01
#           ...
#           (6)[1:50]21|Assim,(6)[1:62]22|Assim,+1,+0:12
#           (7)[2:00]22|Probe,(8)[2:15]22|Probe,0,+0:15
#           (8)[2:10]22|Pylon,(7)[2:00]22|Pylon,0,-0:10
#
#
# order_dev + order_dev_p, time_dev + time_dev_p : scale and average these to derive deviation, as these are the only
#                                                   sub-metrics that matter in determining how well a build is
#                                                   performed.
# discrepency (including additional elements not in bench) : use this for build order detection.


WORKER_NAMES = ['Probe', 'SCV', 'Drone']
ARMY_NAMES = ['Zealot', 'Adept', 'Stalker', 'Sentry', 'DarkTemplar', 'HighTemplar', 'Archon',
              'Observer', 'Immortal', 'WarpPrism', 'Colossus', 'Disruptor',
              'Phoenix', 'VoidRay', 'Oracle', 'Carrier', 'Tempest', 'Mothership']
BUILDING_NAMES = ['Nexus', 'Pylon', 'Assimilator', 'Gateway', 'Forge', 'CyberneticsCore', 'PhotonCannon', 'ShieldBattery',
                  'RoboticsFacility', 'RoboticsBay', 'Stargate', 'FleetBeacon', 'TwilightCouncil', 'TemplarArchives', 'DarkShrine']
UPGRADE_NAMES = ['ProtossGroundWeapons1', 'ProtossGroundWeapons2', 'ProtossGroundWeapons3',
                 'ProtossGroundArmor1', 'ProtossGroundArmor2', 'ProtossGroundArmor3',
                 'ProtossShieldArmor1', 'ProtossShieldArmor2', 'ProtossShieldArmor3',
                 'ProtossAirWeapons1', 'ProtossAirWeapons2', 'ProtossAirWeapons3',
                 'ProtossAirArmor1', 'ProtossAirArmor2', 'ProtossAirArmor3',
                 'WarpGate', 'Charge', 'Blink', 'ResonatingGlaives', 'ShadowStride', 'PsionicStorm', 
                 'ExtendedThermalLance', 'GraviticDrive', 'GraviticBoosters', 'AnionPulseCrystals']


class BuildOrderDeviationElement(object):

    def __init__(self, bench_boe, compare_boe):
        self.bench = bench_boe
        self.compare = compare_boe
        if compare_boe is not None:
            self.order_dev = abs(self.bench.build_num - self.compare.build_num)
            self.time_dev = abs(self.bench.time - self.compare.time)
            self.discrepency = 0
        else:
            self.order_dev = 0
            self.time_dev = 0
            self.discrepency = 1

    def to_csvrow(self):
        return [self.bench.build_num, self.bench.time, self.bench.supply, self.bench.name,
                self.compare.build_num, self.compare.time, self.compare.supply, self.compare.name,
                self.order_dev, self.time_dev, self.discrepency, self.order_dev_p, self.time_dev_p]
           


class BuildOrderDeviation(object):

    # ORDER_DEV_GRACE is used to specify how far a build unit can be in the
    # build order past its corresponding build unit in the benchmark
    # before it can no longer be considered related to that benchmark
    # build unit. Also, allows the compared build order to go this amount
    # of build order units past the last benchmark build unit (or depth).
    ORDER_DEV_GRACE=20

    def __init__(self, bench_bo):
        if len(bench_bo) <= 0:
            raise ValueError('bench_bo does not contain any build order elements.')
        self._bench_bo = bench_bo
        self._initialize()


    def _initialize(self):
        self.dev = 0
        self.time_dev = 0
        self.time_dev_p = 0
        self.order_dev = 0
        self.order_dev_p = 0
        self.discrepency = 0
        self.acc_time_dev = []
        self.acc_order_dev = []
        #self.dev_arr = []
        self.bode_arr = []
        self.tag_order_dev = {}
        self.tag_order_dev_p = {}
        self.bench_depth = len(self._bench_bo)


    # when depth is defined, the calculated depth will be the minimum between depth and bench bo
    # when depth is not defined, the calculated depth is the minimum between bench and compare bo
    def _calculate_depth(self, desired_depth, compare_bo):
        if (desired_depth < 0):
            return min(len(self._bench_bo), len(compare_bo))
        else:
            return min(desired_depth, len(self._bench_bo))


    def _get_unit_category(unit_name):
        if unit_name in WORKER_NAMES:
            return 'worker'

        if unit_name in ARMY_NAMES:
            return 'army'

        if unit_name in BUILDING_NAMES:
            return 'building'

        if unit_name in UPGRADE_NAMES:
            return 'upgrade'
            

    def calculate_deviations(self, compare_bo, depth=-1):
        """Calculates the deviation metrics from the given build order

        Calculates all of the deviation metrics that arise from comparing the given
        build order to the benchmark build order.

        Args:
            compare_bo (BuildOrderElement[]): The build order to compare to the
                benchmark.

            (depth) (int): Optional. The depth with which to traverse the build order. If
                not defined (-1), the entire build order will be used.

        Returns:
            float: The deviation recorded between the builds.
            
        """
        if len(compare_bo) <= 0:
            raise ValueError('compare_bo does not contain any build order elements.')
        
        self._initialize()

        #bo_depth = depth if depth >= 0 and depth < len(self._bench_bo) else len(self._bench_bo)
        bo_depth = self._calculate_depth(depth, compare_bo)
        
        cmp_bo = self._get_sorted_build_order(compare_bo, bo_depth)

        for idx in range(bo_depth):
            bode = BuildOrderDeviationElement(self._bench_bo[idx], cmp_bo[idx])
            self.bode_arr.append(bode)
            unit_tags = get_tags(self._bench_bo[idx].name)

            self.discrepency += bode.discrepency
            if cmp_bo[idx] is not None:
                self.time_dev += bode.time_dev
                self.order_dev += bode.order_dev                
                self.acc_time_dev.append(bode.time_dev)
                self.acc_order_dev.append(bode.order_dev)
                for tg in unit_tags:
                    if tg in self.tag_order_dev:
                        self.tag_order_dev[tg] += bode.order_dev
                    else:
                        self.tag_order_dev[tg] = bode.order_dev
            else:
                self.time_dev_p += abs(self._bench_bo[-1].time - self._bench_bo[idx].time)
                self.order_dev_p += abs(self._bench_bo[-1].build_num - self._bench_bo[idx].build_num)
                for tg in unit_tags:
                    if tg in self.tag_order_dev_p:
                        self.tag_order_dev_p[tg] += abs(self._bench_bo[-1].build_num - self._bench_bo[idx].build_num)
                    else:
                        self.tag_order_dev_p[tg] = abs(self._bench_bo[-1].build_num - self._bench_bo[idx].build_num)

        self.discrepency += self._calculate_additional_bo_units_discrepencies(compare_bo, bo_depth)
        self.dev = (self.get_scaled_time_dev(depth) + self.get_scaled_order_dev(depth)) / 2

        return self.dev


    def get_unit_totals(self, bo=None, depth=-1):
        """Get the total number of each units created in a build

        Finds the total number of each unit made in a given build (or the benchmark build
        if no build is supplied).

        Args:
            bo (dict): (Optional) The build order to extract unit totals from. Uses the
                benchmark build order if no build order is supplied.
            depth (int): (Optional) The depth with which to traverse the build order. If
                not defined (-1), the entire build order will be used.

        Returns:
            (dict): A dictionary of the names of each unit created and the number
                of them created in the entire build.
                
        """
        if bo is None:
            bo = self._bench_bo
        bo_depth = min(len(bo), depth) if depth >= 0 else len(bo)
        bo_trimmed = bo[0:bo_depth]

        build_unit_names = set([boe.name for boe in bo_trimmed])
        name_count = {name: 0 for name in build_unit_names}

        for x in range(bo_depth):
            name_count[bo_trimmed[x].name] += 1

        return name_count


    def get_bench_time(self):
        """Returns the time of the last build order element in the benchmark."""
        return self._bench_bo[-1].time


    def get_bench_total_builds(self):
        """Returns the total number of builds in the benchmark."""
        return self._bench_bo[-1].build_num


    def get_bench_total_supply(self):
        """Returns the supply of the last build order element in the benchmark."""
        return self._bench_bo[-1].supply


    def get_scaled_time_dev(self, depth=-1):
        """Returns the total time deviation scaled to the sum of the time of the
        benchmark."""
        tm = 0
        bo_depth = self._calculate_depth(depth, self._bench_bo)
        bch_bo = self._bench_bo[0:bo_depth]
        tm = sum(bo.time for bo in bch_bo)
        return (self.time_dev + self.time_dev_p) / tm


    def get_scaled_order_dev(self, depth=-1):
        """Returns the total order deviation scaled to the sum of build numbers in the
        benchmark."""
        od = 0
        bo_depth = self._calculate_depth(depth, self._bench_bo)
        bch_bo = self._bench_bo[0:bo_depth]
        od = sum(bo.build_num for bo in bch_bo)
        return (self.order_dev + self.order_dev_p) / od

    
    def get_average_order_dev(self, depth=-1):
        """Returns the average (median) order deviation."""
        ary = []
        for idx in range(len(self.bode_arr)):
            ary.append(self.bode_arr[idx].order_dev)
        ary.sort()
        if len(ary) > 0:
            return ary[int(idx / 2)]
        else:
            return 0


    def get_scaled_discrepency(self, depth=-1):
        """Returns the total discrepencies scaled to the sum of the total number of
        build elements in the benchmark."""
        bo_depth = self._calculate_depth(depth, self._bench_bo)
        bch_bo = self._bench_bo[0:bo_depth]
        dis = len(bch_bo)
        return self.discrepency / dis


    def get_scaled_tag_order_dev(self, tag, depth=-1):
        """Returns the total order deviation of the given tag scaled to the sum of the
        build numbers in the benchmark."""
        od = 0
        bo_depth = self._calculate_depth(depth, self._bench_bo)
        bch_bo = self._bench_bo[0:bo_depth]
        od = sum(bo.build_num for bo in bch_bo)
        tod = self.tag_order_dev[tag] if tag in self.tag_order_dev else 0
        todp = self.tag_order_dev_p[tag] if tag in self.tag_order_dev_p else 0
        return (tod + todp) / od



    def _calculate_additional_bo_units_discrepencies(self, compare_bo, depth=-1):
        disc = 0

        name_count_cmp = self.get_unit_totals(compare_bo, depth)
        name_count_bch = self.get_unit_totals(self._bench_bo, depth)

        for x in name_count_cmp.keys():
            if x in name_count_bch:
                disc += abs(name_count_cmp[x] - name_count_bch[x])
            else:
                disc += name_count_cmp[x]

        return disc
            

    def _bo_units(bo, nm):
        for x in bo:
            if x.name == nm:
                yield x

    def _get_sorted_build_order(self, bo, depth=-1):
        sort_bo = []
        last_build_num = self._calculate_depth(depth, self._bench_bo)

        # create a dictionary of iterators, each iterator returns the next
        # element that matches the build unit name
        build_unit_names = set([boe.name for boe in self._bench_bo])
        iters_of_type = {name: None for name in build_unit_names}
        for nm in build_unit_names:
            #iters_of_type[nm] = (e for i, e in enumerate(bo) if e.name == nm)
            #iters_of_type[nm] = (x for x in bo if x.name == nm)
            iters_of_type[nm] = BuildOrderDeviation._bo_units(bo, nm)
            

        # create a new comparison build order that rearranges the elements
        # based on the order of the benchmark build
        for boe in self._bench_bo:
            tmp_bo = next(iters_of_type[boe.name], None)

            # if the build number is greater than the last build number
            # of the bench, or if the build number difference is greater
            # than 20, then the element is not associated with this part of
            # the build.
            if tmp_bo is not None and tmp_bo.build_num <= last_build_num + self.ORDER_DEV_GRACE and abs(tmp_bo.build_num - boe.build_num) <= self.ORDER_DEV_GRACE:
                sort_bo.append(tmp_bo)
            else:
                sort_bo.append(None)
                iters_of_type[boe.name] = itertools.chain([tmp_bo], iters_of_type[boe.name])

        return sort_bo
        


def get_argument_parser():
    parser = argparse.ArgumentParser(description='Build Order Deviation metric')

    parser.add_argument('player_name', type=str, help='The name of the player to gather the metric data on.')
    parser.add_argument('bench_path', type=str, help='The replay to use as a benchmark for the build order.')
    parser.add_argument('compare_path', type=str, help='The replay(s) to compare against the benchmark build order. Specifying a folder will use all the replays in that folder.')
    parser.add_argument('--bench_player', type=str, help='The name of the player to monitor in the bench replay. If not specified the same name will be used as player_name.')
    parser.add_argument('--depth', type=int, default=-1, help='Specify how deep into the build order to track.')

    parser.add_argument('--output_path', type=str, help='The location to store output files. If not specified, the same location as this program will be used.')
    parser.add_argument('--metric_output', action='store_true', default=False, help='Output a file containing the metric data.')
    parser.add_argument('--dev_array_output', action='store_true', default=False, help='Output a file containing a comparison of each build element.')
    #parser.add_argument('--plot_output', action='store_true', default=False, help='Output files containing plots of the deviation metric for each replay.')
    #parser.add_argument('--all_output', action='store_true', default=False, help='Generate all output files.')
    parser.add_argument('--latest', action='store_true', default=False, help='Parse only the latest replay in a folder.')

    return parser


if __name__ == '__main__':
    import os
    import glob
    import csv
    import argparse
    from metric_containers import *
    from metric_factory.spawningtool_factory import SpawningtoolFactory

    METRIC_OUTPUT_FILENAME = 'metric_output.csv'
    DEV_ARR_OUTPUT_FILENAME = 'dev_array_output.csv'


    parser = get_argument_parser()
    args = parser.parse_args()


    bench_factory = SpawningtoolFactory(args.bench_path)
    bo_bench = bench_factory.generateBuildOrderElements(args.player_name if not args.bench_player else args.bench_player)
    bod = BuildOrderDeviation(bo_bench)


    ## output metric file
    out_met_path = os.path.join(args.output_path, METRIC_OUTPUT_FILENAME) if args.output_path else METRIC_OUTPUT_FILENAME
    out_met_file_exists = os.path.isfile(out_met_path)
    out_met_file = open(out_met_path, 'a', newline='') if args.metric_output else None
    out_met_writer = csv.writer(out_met_file, quoting=csv.QUOTE_MINIMAL) if out_met_file else None
    if out_met_writer and not out_met_file_exists:
        rw = ['deviation', 'scaled time dev', 'scaled order dev', 'depth'] + ReplayMetadata.csv_header() + ['filename']
        out_met_writer.writerow(rw)


##    ## output deviation array
##    out_dev_arr_path = os.path.join(args.output_path, DEV_ARR_OUTPUT_FILENAME) if args.output_path else DEV_ARR_OUTPUT_FILENAME
##    out_dev_arr_file = open(out_dev_arr_path, 'w+', newline='') if args.dev_array_output else None
##    out_dev_arr_writer = csv.writer(out_dev_arr_file, quoting=csv.QUOTE_MINIMAL) if out_dev_arr_file else None
##    if out_dev_arr_writer:
##        rw = ['order_bench', 'time_bench', 'supply_bench', 'name_bench',
##              'order_compare', 'time_compare', 'supply_compare', 'name_compare',
##              'order_dev', 'time_dev', 'discrepency', 'order_dev_p', 'time_dev_p']
##        out_dev_arr_writer.writerow(rw)


    print("depth : ", args.depth if args.depth >= 0 else len(bo_bench))

    replay_paths = []
    if os.path.isdir(args.compare_path):
        if args.latest:
            replay_paths.append(max(glob.iglob(os.path.join(args.compare_path, '*.[Ss][Cc]2[Rr]eplay')), key=os.path.getctime))
        else:
            for pth in os.listdir(args.compare_path):
                if os.path.splitext(pth)[1] == '.SC2Replay':
                    replay_paths.append(os.path.join(args.compare_path, pth))
    else:
        replay_paths.append(args.compare_path)

    for pth in replay_paths:
        fact = SpawningtoolFactory(pth)
        bo_compare = fact.generateBuildOrderElements(args.player_name)
        if len(bo_compare) > 0:
            meta = fact.generateReplayMetadata()
            bod.calculate_deviations(bo_compare, args.depth)
            print(round(bod.dev, 4), ":", meta.to_string())
            if out_met_writer:
                rw = [round(bod.dev, 4), round(bod.get_scaled_time_dev(), 4), round(bod.get_scaled_order_dev(), 4), args.depth if args.depth >= 0 else len(bo_bench)] + meta.to_csv_list() + [os.path.basename(pth)]
                out_met_writer.writerow(rw)
##            if out_dev_arr_writer:
##                for bode in bod.bode_arr:
##                    out_dev_arr_writer.writerow(bode.to_csvrow())
            
    
    if out_met_file:
        out_met_file.close()

    

##def test_things():
##    from metric_containers import *
##    from metric_factory.spawningtool_factory import generateBuildOrderElements
##    from pprint import pprint
##
##    BO_DEPTH=63
##
##    boe_bench = generateBuildOrderElements('../tests/integration/test_replays/pvz_dt_archon_drop_benchmark_bo.SC2Replay', 'Gemini')
##    #boe_exec = generateBuildOrderElements('../tests/integration/test_replays/pvz_dt_archon_drop_executed_bo.SC2Replay', 'NULL')
##    boe_exec = generateBuildOrderElements('../tests/integration/test_replays/pvz_dt_archon_drop_executed_bo_closer.SC2Replay', 'NULL')
##
##    bod = BuildOrderDeviation(boe_bench)
##
##    bod.calculate_deviations(boe_exec, depth=BO_DEPTH)
##
##    pprint(bod.dev_arr)
##
##    #print("supp_dev: ",bod.supp_dev)
##    print("time_dev: ",bod.time_dev)
##    print("order_dev: ",bod.order_dev)
##    print("disc: ", bod.discrepency)
##    #print("supp_dev / supp: ",bod.supp_dev / bod.get_bench_total_supply())
##    #print("time_dev / time: ",bod.time_dev / bod.get_bench_time())
##    #print("order_dev / builds: ", bod.order_dev / bod.get_bench_total_builds())
##    #print("disc / builds: ", bod.discrepency / bod.get_bench_total_builds())
##    print("SCALED time_dev: ", bod.get_scaled_time_dev(depth=BO_DEPTH))
##    #print("SCALED supp_dev: ", bod.get_scaled_supp_dev(depth=BO_DEPTH))
##    print("SCALED order_dev: ", bod.get_scaled_order_dev(depth=BO_DEPTH))
##    #print("SCALED output_eval: ", (bod.get_scaled_discrepency(depth=BO_DEPTH) + bod.get_scaled_time_diff(depth=BO_DEPTH)) / 2)
##    print("BOD: ", bod.dev)
##    pprint(bod.get_unit_totals(depth=63))
##    pprint(bod.get_unit_totals(boe_exec, depth=63))
##
##    import matplotlib.pyplot as plt
##
##    plt.plot(bod.acc_time_dev)
##
##    plt.xlabel('build order')
##    plt.ylabel('time dev (s)')
##    plt.title('Accumulated Time Deviation')
##    plt.grid(True)
##    plt.savefig('acc_time_dev.png')
##    plt.show()
##    
##    roc = []
##    for d in range(1, len(bod.acc_time_dev)):
##        roc.append((bod.acc_time_dev[d] - bod.acc_time_dev[d-1]))
##
##    plt.plot(roc)
##    plt.xlabel('build order')
##    plt.ylabel('ROC of time dev (s/bo)')
##    plt.ylim(top=30)
##    plt.title('ROC of Accumulated Time Deviation')
##    plt.grid(True)
##    plt.savefig('roc_acc_time_dev.png')
##    plt.show()
##
##    # Savitzky-Golay derivative digital filter algorithm
##    sg = []
##    coefficient = (1,-8,0,8,-1)
##    N = 5
##    h = 1
##    for d in range(0, len(bod.acc_time_dev), 5):
##        deriv = 0
##        if d+N < len(bod.acc_time_dev):
##            for i in range(d,d+N):
##                deriv += bod.acc_time_dev[i] * coefficient[i-d]
##            sg.append(deriv / (12 * h))
##
##    plt.plot(sg)
##    plt.xlabel('build order / 5')
##    plt.ylabel('Derivative of time dev (s/bo)')
##    plt.ylim(top=50, bottom=-50)
##    plt.title('Derivative of Accumulated Time Deviation')
##    plt.grid(True)
##    plt.savefig('deriv_acc_time_dev.png')
##    plt.show()

        
    
    
    
