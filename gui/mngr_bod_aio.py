

from metrics.build_order_detect import BuildOrderDetect
from metrics.bod import BuildOrderDeviation

class MngrBodAio(object):

    def __init__(self):
        # todo
        self.dmy = []

    def add_to_build_library(self, build_name, player_name, file_name):
        self.dmy.append("bld")

    def remove_from_build_library(self, build):
        if build:
            self.dmy.remove(build)

    def get_build_library(self):
        return self.dmy

    def get_bod_results_from_replay(self, rep_file_name):
        return ('BOD\r\n'
                '---------\r\n'
                'Blink/Robo : 11.08%\r\n'
                'Chargelot All-in : 4.89%')