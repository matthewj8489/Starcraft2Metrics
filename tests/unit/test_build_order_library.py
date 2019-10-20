import sys

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


from context import metrics
from metrics.build_order_library import BuildOrderLibrary
from metrics.metric_containers import BuildOrder
from metrics.metric_containers import BuildOrderElement


class TestBuildOrderLibrary(unittest.TestCase):

    def get_builds(self):
        blds = []
        blds.append(BuildOrder(name="my_first"))
        blds.append(BuildOrder(name="my_second"))
        blds.append(BuildOrder(name="my_third"))
        return blds

#region build_count

    def test_correct_build_count_is_returned(self):
        bol = BuildOrderLibrary(self.get_builds())

        self.assertEqual(3, bol.build_count())

#endregion

#region get_build

    def test_correct_build_is_returned_when_given_index(self):
        bol = BuildOrderLibrary(self.get_builds())

        bo = bol.get_build_by_index(2)

        self.assertEqual("my_third", bo.name)

    def test_IndexError_is_raised_when_index_is_out_of_range(self):
        bol = BuildOrderLibrary(self.get_builds())

        self.assertRaises(IndexError, bol.get_build_by_index, 3)

    def test_correct_build_is_returned_when_given_name(self):
        bol = BuildOrderLibrary(self.get_builds())

        bo = bol.get_build_by_name("my_second")

        self.assertEqual("my_second", bo.name)

    def test_none_is_returned_when_build_with_name_does_not_exist(self):
        bol = BuildOrderLibrary(self.get_builds())

        bo = bol.get_build_by_name("gggg")

        self.assertIsNone(bo)

    def test_first_build_with_given_name_is_returned_when_multiple_builds_have_the_same_name(self):
        blds = self.get_builds()
        blds[1].build.append(BuildOrderElement(1, "second", 0, 0, 0))
        blds[2].build.append(BuildOrderElement(1, "third", 0, 0, 0))
        blds[2].name = "my_second"

        bol = BuildOrderLibrary(blds)

        bo = bol.get_build_by_name("my_second")

        self.assertEqual("second", bo.build[0].name)
        

#endregion

#region add_build

    def test_build_is_placed_at_the_end_of_the_build_list_when_adding_build(self):
        bol = BuildOrderLibrary(self.get_builds())

        bol.add_build(BuildOrder(name="my_added_build"))

        self.assertEqual("my_added_build", bol.get_build_by_index(bol.build_count()-1).name)

#endregion

#region remove_build

    def test_build_is_removed_when_removing_by_index(self):
        bol = BuildOrderLibrary(self.get_builds())

        bol.remove_build_by_index(1)

        self.assertIsNone(bol.get_build_by_name("my_second"))

    def test_IndexError_is_raised_from_remove_when_index_is_out_of_range(self):
        bol = BuildOrderLibrary(self.get_builds())

        self.assertRaises(IndexError, bol.remove_build_by_index, 3)

    def test_build_is_removed_when_removing_by_name(self):
        bol = BuildOrderLibrary(self.get_builds())

        bol.remove_build_by_name("my_second")

        self.assertIsNone(bol.get_build_by_name("my_second"))

    def test_no_builds_are_removed_if_invalid_name_is_given(self):
        bol = BuildOrderLibrary(self.get_builds())

        bol.remove_build_by_name("gggg")

        self.assertEqual(3, bol.build_count())

    def test_first_build_is_removed_when_removing_by_name_and_multiple_builds_have_the_same_name(self):
        blds = self.get_builds()
        blds[1].build.append(BuildOrderElement(1, "second", 0, 0, 0))
        blds[2].build.append(BuildOrderElement(1, "third", 0, 0, 0))
        blds[2].name = "my_second"

        bol = BuildOrderLibrary(blds)

        bol.remove_build_by_name("my_second")

        self.assertEqual("third", bol.get_build_by_name("my_second").build[0].name)

    def test_build_is_removed_when_removing_by_build(self):
        blds = self.get_builds()
        bol = BuildOrderLibrary(blds)

        bol.remove_build_by_build_order(blds[1])

        self.assertEqual(2, bol.build_count())
        self.assertIsNone(bol.get_build_by_name("my_second"))

    def test_ValueError_is_raised_when_trying_to_remove_a_build_not_in_the_library(self):
        bol = BuildOrderLibrary(self.get_builds())
        bo = BuildOrder()

        self.assertRaises(ValueError, bol.remove_build_by_build_order, bo)

#endregion

#region save_library

#endregion

if __name__ == '__main__':
    unittest.main()
