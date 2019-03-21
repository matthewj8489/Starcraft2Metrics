class Worker(object):

    def __init__(self, second):
        self.second = second

    
class WorkersCreatedTracker(object):

    name = 'WorkersCreatedTracker'


    def handleInitGame(self,event,replay):
        for player in replay.players:
            player.workers_created = []


    def handleUnitBornEvent(self,event,replay):
        if event.unit.is_worker:
            replay.player[event.unit.owner.pid].workers_created.append(
                Worker(event.second))
            
            
