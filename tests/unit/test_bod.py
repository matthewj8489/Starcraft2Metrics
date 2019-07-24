import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
    
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import metrics
from metrics.bod import BuildOrderDeviation
from metrics.metric_containers import *

class TestBuildOrderDeviation(unittest.TestCase):

############################ SUPPLY DEVIATION TESTS ############################
    
    def test_supply_deviation_calculated_correctly_when_late_on_supply(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 16, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.supp_dev, 1)


    def test_supply_deviation_calculated_correctly_when_early_on_supply(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 14, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.supp_dev, 1)


    def test_supply_deviation_calculated_correctly_when_no_supply_deviation_occurred(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.supp_dev, 0)


    def test_supply_deviation_calculated_correctly_when_build_order_deviation_occurred(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))
        compare_bo.append(BuildOrderElement(3, 'Pylon', 16, 60, 220))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.supp_dev, 2)


    def test_supply_deviation_isnt_affected_when_build_order_deviates_by_more_than_20(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))
        compare_bo.append(BuildOrderElement(23, 'Pylon', 14, 20, 90))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.supp_dev, 0)        


    def test_supply_deviation_calculated_correctly_when_build_is_missing_element(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.supp_dev, 0)        
        

############################ TIME DEVIATION TESTS ############################

    def test_time_deviation_calculated_correctly_when_late_on_time(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 60, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.time_dev, 10)

    def test_time_deviation_calculated_correctly_when_early_on_time(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 40, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.time_dev, 10)


    def test_time_deviation_calculated_correctly_when_no_time_deviation(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.time_dev, 0)

    
    def test_time_deviation_calculated_correctly_when_build_order_deviation_occurred(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))
        compare_bo.append(BuildOrderElement(3, 'Pylon', 16, 60, 220))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.time_dev, 40)


    def test_time_deviation_calculated_correctly_when_build_is_missing_element(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        #self.assertEqual(bo_dev.time_dev, 30)
        self.assertEqual(bo_dev.time_dev, 0)


    def test_time_deviation_isnt_affected_when_build_order_deviates_by_more_than_20(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(23, 'Pylon', 14, 25, 90))
        compare_bo.append(BuildOrderElement(24, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        #self.assertEqual(bo_dev.time_dev, 30)
        self.assertEqual(bo_dev.time_dev, 0)
        

    def test_time_deviation_isnt_affected_when_build_order_deviates_by_more_than_20_beyond_last_build_unit(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))
        compare_bo.append(BuildOrderElement(24, 'Pylon', 14, 20, 90))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        #self.assertEqual(bo_dev.time_dev, 30)
        self.assertEqual(bo_dev.time_dev, 0)


############################ TEST DEVIATION ARRAY ############################

    def test_dev_arr_is_correct_size_when_build_order_is_correct(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))
        
        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(3, len(bo_dev.dev_arr))
        


############################ TEST Nth BUILD NUM LIMITOR ############################

    def test_build_order_comparison_is_limited_when_setting_build_num_limitor(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 16, 51, 201))
        

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo, depth=2)

        self.assertEqual(bo_dev.time_dev, 0)


############################ TEST ORDER DEVIATION ############################

    def test_order_deviation_calculated_correctly_when_no_deviation(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.order_dev, 0)

    
    def test_order_deviation_calculated_correctly_when_build_order_deviation_occurred(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))
        compare_bo.append(BuildOrderElement(3, 'Pylon', 16, 60, 220))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.order_dev, 2)


    def test_order_deviation_calculated_correctly_when_build_is_missing_element(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.order_dev, 1)


    def test_order_deviation_isnt_affected_when_build_order_deviates_by_more_than_20(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(23, 'Pylon', 14, 25, 90))
        compare_bo.append(BuildOrderElement(24, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.order_dev, 0)
        

    def test_order_deviation_isnt_affected_when_build_order_deviates_by_more_than_20_beyond_last_build_unit(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))
        compare_bo.append(BuildOrderElement(24, 'Pylon', 14, 20, 90))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.order_dev, 0)
        
        
if __name__ == '__main__':
    unittest.main()
