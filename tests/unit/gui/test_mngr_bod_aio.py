import sys

# unit test
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from unittest.mock import MagicMock
from unittest.mock import patch

# import gui
from context import metrics
from metrics.gui.mngr_bod_aio import MngrBodAio
from metrics.metric_factory.i_build_order_factory import IBuildOrderFactory
from metrics.metric_containers import BuildOrder
from metrics.metric_containers import BuildOrderElement
from metrics.build_order_library import BuildOrderLibrary

class MockBuildOrderFactory(IBuildOrderFactory):

    def __init__(self):
        self.build = BuildOrder(name="Mock")

    def generateBuildOrder(self, player_name, file_name, build_name=''):
        self.build.name = build_name
        return self.build

class MockBuildOrderLibrary(BuildOrderLibrary):

    def __init__(self, build, confidence, bod):
        self.mock_build = build
        self.mock_confidence = confidence
        self.mock_bod = bod

    def get_closest_matching_build(self, build):
        return self.mock_build, self.mock_confidence, self.mock_bod

class TestMngrBodAio(unittest.TestCase):

#region add_to_build_library

    def test_build_is_added_to_library(self):
        bol = BuildOrderLibrary()
        fact = MockBuildOrderFactory()
        mngr = MngrBodAio(bol, fact, "")

        mngr.add_to_build_library("my_build", "my_player", "my_file")

        self.assertEqual(1, bol.build_count())
        self.assertEqual(fact.build, bol.get_build_by_index(0))


#endregion

#region remove_from_build_library

#endregion

#region get_builds

#endregion

#region get_bod_results_from_replay

    def test_returns_correct_string_from_bod_results_from_replay(self):
        bol = MockBuildOrderLibrary(BuildOrder(name="my_mock_build"), 0.95678, MagicMock(dev=0.15))
        fact = MockBuildOrderFactory()
        mngr = MngrBodAio(bol, fact, "")

        res = mngr.get_bod_results_from_replay("C:\my_replay.SC2Replay", "my_mock_name")

        self.assertEqual("my_replay.SC2Replay\r\n--------\r\nbuild: my_mock_build\r\nconfidence: 95.68%\r\ndeviation: 15.00%\r\n\r\n", res)


#endregion

if __name__ == '__main__':
    unittest.main()
