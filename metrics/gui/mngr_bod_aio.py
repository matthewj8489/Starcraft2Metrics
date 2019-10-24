class MngrBodAio(object):

    def __init__(self, build_lib, bo_fact, build_lib_filepath):
        """Constructor

        Initializes the manager.

        Args:
            build_lib (BuildOrderLibrary):   A library of known builds.

            bo_fact (IBuildOrderFactory): A factory to generate build orders from a replay file.

        """
        self._build_lib = build_lib
        self._bo_fact = bo_fact
        self._build_lib_filepath = build_lib_filepath

    def add_to_build_library(self, build_name, player_name, file_name):
        """Add build to build library

        Adds the build contained in the replay file by the player to the build library.

        Args:
            build_name (str): The name to associate with the build.

            player_name (str): The name of the player in the replay to extract the build from.

            file_name (str): The complete path to the .SC2Replay replay file.

        """
        bo = self._bo_fact.generateBuildOrder(player_name, file_name, build_name)
        self._build_lib.add_build(bo)

    def remove_from_build_library(self, build):
        self._build_lib.remove_build_by_build_order(build)

    def get_builds(self):
        return self._build_lib.get_builds()

    def get_bod_results_from_replay(self, rep_file_name, player_name):
        closest_match_build = None
        confidence = 0
        bo_dev = None

        # get a build order from the replay file and player name
        bo = self._bo_fact.generateBuildOrder(player_name, rep_file_name)

        # get the closest build from the build library
        closest_match_build, confidence, bo_dev = self._build_lib.get_closest_matching_build(bo)

        return "build: {} | confidence: {} | deviation: {}".format(closest_match_build.name, confidence, bo_dev.dev)

    def save_build_library(self):
        self._build_lib.save_library(self._build_lib_filepath)