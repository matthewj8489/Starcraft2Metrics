class Base(object):

    def __init__(self, second):
        self.second = second


class BasesCreatedTracker(object):

    name = 'BasesCreatedTracker'


    def __init__(self):
        self._base_names = [
            'Nexus',
            'CommandCenter',
            'Hatchery'
            ]


    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.bases_created = []


    def handleUnitDoneEvent(self,event,replay):
        if event.unit.is_building and (event.unit.name in self._base_names):
            replay.player[event.unit.owner.pid].bases_created.append(
                Base(event.second))
