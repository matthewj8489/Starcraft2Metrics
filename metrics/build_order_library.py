import json
import copy
from metrics.build_order_detect import BuildOrderDetect
from metrics.metric_containers import BuildOrder

class BuildOrderLibrary(object):

    def __init__(self, builds=[]):
        self._builds = builds

    def get_builds(self):
        return self._builds

    def build_count(self):
        """Returns the number of builds contained in the library."""
        return len(self._builds)

    def get_build_by_index(self, index):
        """Returns the build order at the specified index

        Args:
            index (int): The index of the desired build in the library

        Returns:
            BuildOrder: A BuildOrder object containing the build.

        Raises:
            IndexError: If an invalid index is given.

        """
        if index < len(self._builds):
            return self._builds[index]
        else:
            raise IndexError("Index was out of range of the build order library.")

    def get_build_by_name(self, name):
        """Returns the first build order with the specified name

        Args:
            name (str): The name of the desired build in the library

        Returns:
            BuildOrder: A BuildOrder object containing the build or None if a build with the name doesn't exist.

        """
        return next((x for x in self._builds if x.name == name), None)

    def add_build(self, build):
        """Add a build to the build library

        Args:
            build (BuildOrder): The build to add to the library.

        """
        self._builds.append(build)

    def remove_build_by_index(self, index):
        """Removes a build at the specified index

        Args:
            index (int): The index of the build to remove from the library.

        """
        del self._builds[index]

    def remove_build_by_name(self, name):
        """Removes the first build with the specified name

        Args:
            name (str): The name of the build to remove

        """
        bld = next((x for x in self._builds if x.name == name), None)
        if bld:
            self._builds.remove(bld)

    def remove_build_by_build_order(self, build):
        """Removes the specified build
        Args:
            build (BuildOrder): The build to remove from the library

        """
        self._builds.remove(build)

    def save_library(self, filename):
        """Saves the build library to a json file

        Args:
            filename (str): The full file name and path to store the library into.

        Raises:
            FileNotFoundError: If an invalid path is given.

        """
        j_builds = []
        for bld in self._builds:
            j_builds.append(bld.serialize())

        with open(filename, 'w') as bch_fl:
            json.dump(j_builds, bch_fl)

    def load_library(self, filename):
        """Loads the library from a valid json file.

        Args:
            filename (str): The full file name and path to load the library from.

        Raises:
            FileNotFoundError: If an invalid path is given.

        """
        self._builds = []
        with open(filename, 'r') as bch_fl:
            j_builds = json.load(bch_fl)
            for j_bld in j_builds:
                bld = BuildOrder()
                bld.deserialize(copy.deepcopy(j_bld))
                self._builds.append(bld)
        

    def get_closest_matching_build(self, build):
        """Returns the closest build in the library to the given build.

        Args:
            build (BuildOrder): The build to find the closest match to.

        Returns:
            BuildOrder: The closest build in the library.
            int:        The confidence that the given build is the same as the returned build.
            BuildOrderDeviation:    The BOD object used to determine the confidence.

        """
        closest_build = None
        closest_confidence = 0
        closest_build_bod = None

        # loop through all builds in the build library and run detect_build_order
        # to determine the confidence that the replay build order is the same as 
        # the one in the build library
        for bld in self._builds:
            conf, bod = BuildOrderDetect.detect_build_order(bld.build, build.build)
            if conf > closest_confidence:
                closest_build = bld
                closest_confidence = conf
                closest_build_bod = bod

        return closest_build, closest_confidence, closest_build_bod