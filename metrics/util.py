import sc2reader

def convert_realtime_to_gametime(real_time_s, game_frames, game_fps, game_length_s):
    game_time = 0

    real_fps = game_frames / game_length_s
    real_game_frame = real_time_s * real_fps
    game_time = real_game_frame // game_fps

    return game_time


def convert_realtime_to_gametime_r(replay, real_time_s):
    '''
    Converts the real time of a point in the replay to the internally calculated game time.

    Keyword arguments:
    replay -- the sc2reader replay object from which to convert the real time to.
    real_time_s -- the real time in the replay in seconds.
    '''
    return convert_realtime_to_gametime(real_time_s, replay.frames, replay.game_fps, replay.game_length.seconds)
