import itertools

# Outputs:
# dev - a metric that weights supply differences, time differences, order
#       differences, and build discrepencies combined, 0 is a perfectly
#       executed build order.
#       (weight1 * metric1 + weight2 * metric2) / (weight1 + weight2)
#       divide by number of build order elements to normalize by length
#       of build order?
#       Defining weights:
#           Principal component analysis
#           Linear discriminant analysis
#           Naive Bayes classifier
#           create a benchmark of total units (building and army/worker)
#               created by a point in time and then compare that to the
#               bench bo to see how much different metrics affect the
#               differences in the end result of units
# supp_dev  - total deviation in supply (absolute values?)
# time_dev  - total deviation in time (absolute values?)
# order_dev - total deviation in order (absolute values?)
# discrepency   - total discrepencies in build (elements missing or elements
#               that shouldn't be there)
# worst_dev - the worst deviation in the build
# acc_supp_dev  - the accumulated deviation in supply vs bench build ordering
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

class BuildOrderDeviation(object):

    def __init__(self, bench_bo):
        self._bench_bo = bench_bo
        self._initialize()

    def _initialize(self):
        #self.dev = 0
        self.supp_dev = 0
        self.time_dev = 0
        self.order_dev = 0
        #self.discrepency = 0
        #self.worst_dev = None
        self.acc_time_dev = []
        #self.acc_time_dev = []
        #self.acc_order_dev = []
        self.dev_arr = []

    def calculate_deviations(self, compare_bo, depth=-1):
        self._initialize()
        
        cmp_bo = self._get_sorted_build_order(compare_bo, depth)

        for idx in range(depth if depth >= 0 else len(self._bench_bo)):
            if cmp_bo[idx] is not None:
                self.supp_dev += abs(self._bench_bo[idx].supply - cmp_bo[idx].supply)
                self.time_dev += abs(self._bench_bo[idx].time - cmp_bo[idx].time)
                self.order_dev += abs(self._bench_bo[idx].build_num - cmp_bo[idx].build_num)
                self.acc_time_dev.append(self.time_dev)
                self.dev_arr.append([self._bench_bo[idx].to_string(),
                                     cmp_bo[idx].to_string(),
                                     cmp_bo[idx].supply - self._bench_bo[idx].supply,
                                     cmp_bo[idx].time - self._bench_bo[idx].time])
            else:
                #self.time_dev += abs(self._bench_bo[idx].time - self._bench_bo[-1].time)
                #self.acc_time_dev.append(self.time_dev)
                self.dev_arr.append([self._bench_bo[idx].to_string(),
                                     '',
                                     0,
                                     0])#self._bench_bo[-1].time - self._bench_bo[idx].time])


    def _bo_units(bo, nm):
        for x in bo:
            if x.name == nm:
                yield x

    def _get_sorted_build_order(self, bo, depth=-1):
        sort_bo = []
        last_build_num = depth if depth >= -1 else self._bench_bo[-1].build_num

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
            if tmp_bo is not None and tmp_bo.build_num <= last_build_num + 20 and abs(tmp_bo.build_num - boe.build_num) <= 20:
                sort_bo.append(tmp_bo)
            else:
                sort_bo.append(None)
                iters_of_type[boe.name] = itertools.chain([tmp_bo], iters_of_type[boe.name])

        return sort_bo
        


    def detect_build_order(self, compare_bo):
        confidence = 0
        deviation = 0
        #deviation = calculate_deviation(golden_bo, compare_bo)

        return [confidence, deviation]


if __name__ == '__main__':
    from metric_containers import *
    from metric_factory.spawningtool_factory import generateBuildOrderElements
    from pprint import pprint

    boe_bench = generateBuildOrderElements('../tests/integration/test_replays/pvz_dt_archon_drop_benchmark_bo.SC2Replay', 'Gemini')
    #boe_exec = generateBuildOrderElements('../tests/integration/test_replays/pvz_dt_archon_drop_executed_bo.SC2Replay', 'NULL')
    boe_exec = generateBuildOrderElements('../tests/integration/test_replays/pvz_dt_archon_drop_executed_bo_closer.SC2Replay', 'NULL')

    bod = BuildOrderDeviation(boe_bench)

    bod.calculate_deviations(boe_exec, depth=63)

    pprint(bod.dev_arr)

    print(bod.supp_dev)
    print(bod.time_dev)
    print(bod.order_dev)

    import matplotlib.pyplot as plt

    plt.plot(bod.acc_time_dev)

    plt.xlabel('build order')
    plt.ylabel('time dev (s)')
    plt.title('Accumulated Time Deviation')
    plt.grid(True)
    plt.savefig('acc_time_dev.png')
    plt.show()
    
    roc = []
    for d in range(1, len(bod.acc_time_dev)):
        roc.append((bod.acc_time_dev[d] - bod.acc_time_dev[d-1]))

    plt.plot(roc)
    plt.xlabel('build order')
    plt.ylabel('ROC of time dev (s/bo)')
    plt.ylim(top=30)
    plt.title('ROC of Accumulated Time Deviation')
    plt.grid(True)
    plt.savefig('roc_acc_time_dev.png')
    plt.show()

    # Savitzky-Golay derivative digital filter algorithm
    sg = []
    coefficient = (1,-8,0,8,-1)
    N = 5
    h = 1
    for d in range(0, len(bod.acc_time_dev), 5):
        deriv = 0
        if d+N < len(bod.acc_time_dev):
            for i in range(d,d+N):
                deriv += bod.acc_time_dev[i] * coefficient[i-d]
            sg.append(deriv / (12 * h))

    plt.plot(sg)
    plt.xlabel('build order / 5')
    plt.ylabel('Derivative of time dev (s/bo)')
    plt.ylim(top=50, bottom=-50)
    plt.title('Derivative of Accumulated Time Deviation')
    plt.grid(True)
    plt.savefig('deriv_acc_time_dev.png')
    plt.show()

        
    
    
    
