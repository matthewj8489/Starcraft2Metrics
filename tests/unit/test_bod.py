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
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

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
        


############################ TEST DEPTH BUILD NUM LIMITOR ############################

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

        self.assertEqual(bo_dev.dev, 0)
        self.assertEqual(bo_dev.discrepency, 0)


    def test_depth_when_depth_is_greater_than_compare_bo(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
                

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo, depth=3)

        self.assertEqual(bo_dev.dev, 0)
        self.assertEqual(bo_dev.discrepency, 1)
        

    def test_depth_when_depth_is_greater_than_bench_bo(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        
        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 16, 51, 201))
        

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo, depth=3)

        self.assertEqual(bo_dev.dev, 0)
        self.assertEqual(bo_dev.discrepency, 0)

        

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

        self.assertEqual(bo_dev.order_dev, 0)
        

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


############################ TEST DISCREPENCIES ############################

    def test_discrepencies_when_not_missing_build_order_units(self):
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

        self.assertEqual(bo_dev.discrepency, 0)

        
    def test_discrepencies_when_missing_build_order_units(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))
        
        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo, depth=3)

        self.assertEqual(bo_dev.discrepency, 1)


    def test_discrepencies_are_none_when_additional_build_order_units_are_present_beyond_bench_bo(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))
        compare_bo.append(BuildOrderElement(4, 'Pylon', 16, 51, 201))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.discrepency, 0)

    def test_discrepencies_when_additional_build_order_units_are_present(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        compare_bo.append(BuildOrderElement(3, 'Pylon', 14, 25, 100))
        compare_bo.append(BuildOrderElement(4, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.discrepency, 1)


############################ TEST UNIT TOTALS ############################

    def test_unit_totals_are_calculated_correctly_for_bench(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        golden_totals = bo_dev.get_unit_totals()

        self.assertEqual(golden_totals['Probe'], 1)
        self.assertEqual(golden_totals['Pylon'], 1)
        self.assertEqual(golden_totals['Assimilator'], 1)


    def test_unit_totals_are_calculated_correctly_for_any_build_order(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        compare_bo.append(BuildOrderElement(3, 'Pylon', 14, 25, 100))
        compare_bo.append(BuildOrderElement(4, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        compare_totals = bo_dev.get_unit_totals(bo=compare_bo)

        self.assertEqual(compare_totals['Probe'], 1)
        self.assertEqual(compare_totals['Pylon'], 2)
        self.assertEqual(compare_totals['Assimilator'], 1)


    def test_unit_totals_are_correct_when_using_depth(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))
        golden_bo.append(BuildOrderElement(4, 'Pylon', 15, 60, 220))

        bo_dev = BuildOrderDeviation(golden_bo)
        golden_totals = bo_dev.get_unit_totals(depth=3)

        self.assertEqual(golden_totals['Probe'], 1)
        self.assertEqual(golden_totals['Pylon'], 1)
        self.assertEqual(golden_totals['Assimilator'], 1)
        

    def test_unit_totals_do_not_include_units_with_zero_totals_when_using_depth(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))
        golden_bo.append(BuildOrderElement(4, 'Pylon', 15, 60, 220))
        golden_bo.append(BuildOrderElement(5, 'Zealot', 15, 70, 240))

        bo_dev = BuildOrderDeviation(golden_bo)
        golden_totals = bo_dev.get_unit_totals(depth=3)

        self.assertFalse('Zealot' in golden_totals)


############################ TEST TIME DEV PLUS ############################

    def test_time_dev_p_is_correct_when_build_unit_is_missing(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 15, 55, 205))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.time_dev_p, 30)


    def test_time_dev_p_is_zero_when_build_unit_is_not_missing(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Pylon', 14, 25, 95))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 15, 55, 205))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.time_dev_p, 0)

        
    def test_time_dev_p_is_correct_when_build_unit_is_not_missing_but_greater_than_ORDER_DEV_GRACE(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 16, 55, 205))
        compare_bo.append(BuildOrderElement(23, 'Pylon', 17, 65, 215))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.time_dev_p, 30)


############################ TEST ORDER DEV PLUS ############################

    def test_order_dev_p_is_correct_when_build_unit_is_missing(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 16, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.order_dev_p, 1)


    def test_order_dev_p_is_zero_when_build_unit_is_not_missing(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Pylon', 15, 25, 95))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 16, 55, 205))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.order_dev_p, 0)


    def test_order_deviation_calculated_correctly_when_build_has_different_element(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Probe', 14, 20, 90))
        compare_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.order_dev_p, 1)


    def test_order_dev_p_is_correct_when_build_unit_is_not_missing_but_greater_than_ORDER_DEV_GRACE(self):
        golden_bo = []
        compare_bo = []
        golden_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        golden_bo.append(BuildOrderElement(2, 'Pylon', 14, 20, 90))
        golden_bo.append(BuildOrderElement(3, 'Assimilator', 15, 50, 200))

        compare_bo.append(BuildOrderElement(1, 'Probe', 12, 0, 0))
        compare_bo.append(BuildOrderElement(2, 'Assimilator', 16, 55, 205))
        compare_bo.append(BuildOrderElement(23, 'Pylon', 17, 65, 215))

        bo_dev = BuildOrderDeviation(golden_bo)
        bo_dev.calculate_deviations(compare_bo)

        self.assertEqual(bo_dev.order_dev_p, 1)


############################ TEST DEVIATION ############################

    def test_deviation_is_zero_when_builds_are_exactly_the_same(self):
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

        self.assertEqual(bo_dev.dev, 0)


        
if __name__ == '__main__':
    unittest.main()
