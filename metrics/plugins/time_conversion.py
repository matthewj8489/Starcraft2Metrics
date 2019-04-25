

class TimeConverter(object):

    name = 'TimeConverter'
    
    def handleInitGame(self, event, replay):
        replay.game_to_real_time_multiplier = replay.game_fps * replay.game_length.seconds / replay.frames
        replay.real_to_game_time_multiplier = replay.frames / (replay.game_fps * replay.game_length.seconds)