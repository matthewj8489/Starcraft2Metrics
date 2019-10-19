from abc import ABC, abstractmethod

class IBuildOrderFactory(ABC):

    @abstractmethod
    def generateBuildOrder(self, player_name, file_name, build_name=''):
        yield