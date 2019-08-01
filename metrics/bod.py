import itertools
import math

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
                 'WarpGate', 'Charge', 'Blink', 'Glaives', 'ShadowStride', 'PsionicStorm', 'ExtendedThermalLance', 'GraviticDrive']


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
        self.dev_arr = []


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
            if cmp_bo[idx] is not None:
                self.time_dev += abs(self._bench_bo[idx].time - cmp_bo[idx].time)
                self.order_dev += abs(self._bench_bo[idx].build_num - cmp_bo[idx].build_num)
                self.acc_time_dev.append(self.time_dev)
                self.acc_order_dev.append(self.order_dev)
                self.dev_arr.append([self._bench_bo[idx].to_string(),
                                     cmp_bo[idx].to_string(),
                                     cmp_bo[idx].supply - self._bench_bo[idx].supply,
                                     cmp_bo[idx].time - self._bench_bo[idx].time])
            else:
                self.time_dev_p += abs(self._bench_bo[-1].time - self._bench_bo[idx].time)
                self.order_dev_p += abs(self._bench_bo[-1].build_num - self._bench_bo[idx].build_num)
                self.discrepency += 1
                self.dev_arr.append([self._bench_bo[idx].to_string(),
                                     '',
                                     0,
                                     0])#self._bench_bo[-1].time - self._bench_bo[idx].time])

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


    def _nn_feed_forward(self, order, disc):
        NN_WI1 = -0.8326388182288694
        NN_WI2 = -7.0693717100666690
        NN_BI = 0.8541325726369238
        NN_WH = 19.123065721771997
        NN_BH = 0.20449835272881134

        h = 1 / (1 + math.exp(-(order * NN_WI1 + disc * NN_WI2 + NN_BI)))
        out = 1 / (1 + math.exp(-(h * NN_WH + NN_BH)))

        return out

##------
##* Inputs: 2
##------
##Hidden Layer
##Neurons: 2
## Neuron 0
##  Weight: 8.338633843804
##  Weight: -1.5270798061037594
##  Bias: 0.9785443288439529
## Neuron 1
##  Weight: -13.711848744765582
##  Weight: 1.835616004688895
##  Bias: 0.9785443288439529
##------
##* Output Layer
##Neurons: 1
## Neuron 0
##  Weight: -8.431803459641838
##  Weight: 20.56901232827286
##  Bias: 0.8140641980822715
##------
    def _nn2_feed_forward(self, order, disc):
        return 0

    def detect_build_order(self, compare_bo, depth=-1):
        """Determines how likely a build order is modeled after the benchmark build.

        Determines the confidence that the given build order is modeled after the
        benchmark build order contained here.

        Args:
            compare_bo (BuildOrderElement[]): An array of BuildOrderElements to
                determine if it closely matches the benchmark build order.
                
            (depth) (int): Optional. The depth with which to traverse the build order. If
                not defined (-1), the entire build order will be used.

        Returns:
            int: The confidence (0.0 - 1.0) that the given build order is a derivative
                of the benchmark build order.
                
        """
        self.calculate_deviations(compare_bo, depth)
        order_dev = self.get_scaled_order_dev()
        ## there could be more accuracy if the discrepencies were split into 4 categories:
        ## worker, army, building, upgrade and a NN trained on those inputs instead.
        discrepencies = self.get_scaled_discrepency()

        confidence = self._nn_feed_forward(order_dev, discrepencies)

        return confidence


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


    def get_scaled_discrepency(self, depth=-1):
        """Returns the total discrepencies scaled to the sum of the total number of
        build elements in the benchmark."""
        bo_depth = self._calculate_depth(depth, self._bench_bo)
        bch_bo = self._bench_bo[0:bo_depth]
        dis = len(bch_bo)
        return self.discrepency / dis


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
    parser.add_argument('--bench_player', type=str, help='The name of the player to monitor in the bench replay. If not specified the same name will be used as player_name.')
    parser.add_argument('--depth', type=int, default=-1, help='Specify how deep into the build order to track.')
    parser.add_argument('--out_met_file', type=str, help='The filepath to save a .csv file containing the metric data.')
    parser.add_argument('compare_path', type=str, help='The replay(s) to compare against the benchmark build order. Specifying a folder will use all the replays in that folder.')

    #parser.add_argument('--output_path', type=str, help='The location to store output files. If not specified, the same location as this program will be used.')
    #parser.add_argument('--metric_output', action='store_true', default=False, help='Output a file containing the metric data.')
    #parser.add_argument('--dev_array_output', action='store_true', default=False, help='Output a file containing a comparison of each build element.')
    #parser.add_argument('--plot_output', action='store_true', default=False, help='Output files containing plots of the deviation metric for each replay.')
    #parser.add_argument('--all_output', action='store_true', default=False, help='Generate all output files.')

    return parser
    

if __name__ == '__main__':
    import os
    import csv
    import argparse
    from metric_containers import *
    from metric_factory.spawningtool_factory import SpawningtoolFactory

    parser = get_argument_parser()
    args = parser.parse_args()

    bench_factory = SpawningtoolFactory(args.bench_path)
    bo_bench = bench_factory.generateBuildOrderElements(args.player_name if not args.bench_player else args.bench_player)
    bod = BuildOrderDeviation(bo_bench)

    out_met_file = open(args.out_met_file, 'w+', newline='') if args.out_met_file else None
    out_met_writer = csv.writer(out_met_file, quoting=csv.QUOTE_MINIMAL) if out_met_file else None
    if out_met_writer:
        rw = ['deviation', 'scaled time dev', 'scaled order dev', 'depth', 'confidence'] + ReplayMetadata.csv_header() + ['filename']
        out_met_writer.writerow(rw)

    print("depth : ", args.depth if args.depth >= 0 else len(bo_bench))

    replay_paths = []
    if os.path.isdir(args.compare_path):
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
            confidence = bod.detect_build_order(bo_compare, args.depth)
            print(round(bod.dev, 4), ":", round(confidence, 4), ":", meta.to_string())
            if out_met_writer:
                rw = [round(bod.dev, 4), round(bod.get_scaled_time_dev(), 4), round(bod.get_scaled_order_dev(), 4), args.depth if args.depth >= 0 else len(bo_bench), round(confidence, 4)] + meta.to_csv_list() + [os.path.basename(pth)]
                out_met_writer.writerow(rw)
    
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

        
    
    
    
