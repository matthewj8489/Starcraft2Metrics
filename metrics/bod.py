
# Outputs:
# dev - a metric that weights supply differences, time differences, order
#       differences, and build discrepencies combined, 0 is a perfectly
#       executed build order.
# supp_dev  - total deviation in supply (absolute values?)
# time_dev  - total deviation in time (absolute values?)
# order_dev - total deviation in order (absolute values?)
# discrepency   - total discrepencies in build (elements missing or elements
#               that shouldn't be there)
# worst_dev - the worst deviation in the build
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
        self.dev = 0
        self.supp_dev = 0
        self.time_dev = 0
        self.order_dev = 0
        self.discrepency = 0
        self.worst_dev = None
        self.dev_arr = []

    def calculate_deviations(self, compare_bo):
        self._initialize()
        
        cmp_bo = self._get_sorted_build_order(compare_bo)
        #shortest_bo = len(self._bench_bo) if len(self._bench_bo) < len(compare_bo) else len(compare_bo)

        for idx in range(len(self._bench_bo)):
            if cmp_bo[idx] is not None:
                self.supp_dev += abs(self._bench_bo[idx].supply - cmp_bo[idx].supply)
                self.time_dev += abs(self._bench_bo[idx].time - cmp_bo[idx].time)


    def _bo_units(bo, nm):
        for x in bo:
            if x.name == nm:
                yield x

    def _get_sorted_build_order(self, bo):
        sort_bo = []

        # create a dictionary of iterators, each iterator returns the next
        # element that matches the build unit name
        build_unit_names = set([boe.name for boe in self._bench_bo])
        iters_of_type = {name: None for name in build_unit_names}
        for nm in build_unit_names:
            #iters_of_type[nm] = (e for i, e in enumerate(bo) if e.name == nm)
            iters_of_type[nm] = (x for x in bo if x.name == nm)
            #iters_of_type[nm] = BuildOrderDeviation._bo_units(bo, nm)
            

        # create a new comparison build order that rearranges the elements
        # based on the order of the benchmark build
        for boe in self._bench_bo:
            sort_bo.append(next(iters_of_type[boe.name], None))

        return sort_bo
        


    def detect_build_order(self, compare_bo):
        confidence = 0
        deviation = 0
        #deviation = calculate_deviation(golden_bo, compare_bo)

        return [confidence, deviation]


if __name__ == '__main__':
    from metric_containers import *
    golden_bo = []
    compare_bo = []
    golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
    golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
    golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

    compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
    compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

    bo_dev = BuildOrderDeviation(golden_bo)
    bo_dev.calculate_deviations(compare_bo)

    print(bo_dev.time_dev)
    print(bo_dev.supp_dev)
    
    
