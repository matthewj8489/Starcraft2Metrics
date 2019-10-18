from metrics.build_order_detect import BuildOrderDetect
from metrics.bod import BuildOrderDeviation

class MngrBodAio(object):

    def __init__(self, build_lib, bo_fact):
        """Constructor

        Initializes the manager.

        Args:
            build_lib (BuildOrder[]):   A library of known builds.

            bo_fact (IBuildOrderFactory): A factory to generate build orders from a replay file.

        """
        self._build_lib = build_lib
        self._bo_fact = bo_fact

    def add_to_build_library(self, build_name, player_name, file_name):
        """Add build to build library

        Adds the build contained in the replay file by the player to the build library.

        Args:
            build_name (str): The name to associate with the build.

            player_name (str): The name of the player in the replay to extract the build from.

            file_name (str): The complete path to the .SC2Replay replay file.

        """
        yield

    def remove_from_build_library(self, build):
        yield

    def get_build_library(self):
        yield

    def get_bod_results_from_replay(self, rep_file_name):
        yield