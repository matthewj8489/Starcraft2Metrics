from collections import defaultdict


class ArmyCount(object):

    def __init__(self, second, supply):
        self.second = second
        self.supply = supply


class ArmyCreatedTracker(object):

    name = 'ArmyCreatedTracker'


    def __init__(self):
        self._army_created = defaultdict(int)


    def _add_to_army(self,event,replay):
        self._army_created[event.unit.owner.pid] += event.unit.supply
        replay.player[event.unit.owner.pid].army_created.append(
            ArmyCount(event.second, self._army_created[event.unit.owner.pid]))


    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.army_created = []
            self._army_created[player.pid] = 0


    def handleUnitBornEvent(self,event,replay):
        if event.unit.is_army and not event.unit.hallucinated:
            self._add_to_army(event,replay)


    def handleUnitInitEvent(self,event,replay):
        if event.unit.is_army and not event.unit.hallucinated:
            self._add_to_army(event,replay)
