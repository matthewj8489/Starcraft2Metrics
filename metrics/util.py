import sc2reader


def gametime_to_realtime_constant_r(replay):
    return replay.game_fps * replay.game_length.seconds / replay.frames


def realtime_to_gametime_constant_r(replay):
    return 1 / gametime_to_realtime_constant_r(replay)


def convert_realtime_to_gametime(real_time_s, game_frames,
                                 game_fps, game_length_s):
    game_time = 0

    real_fps = game_frames / game_length_s
    real_game_frame = real_time_s * real_fps
    game_time = real_game_frame // game_fps

    return game_time


def convert_realtime_to_gametime_r(replay, real_time_s):
    '''
    Converts the real time of a point in the replay to the internally
    calculated game time.

    Keyword arguments:
    replay -- the sc2reader replay object from which to convert the
              real time to.
    real_time_s -- the real time in the replay in seconds.
    '''
    return convert_realtime_to_gametime(real_time_s, replay.frames,
                                        replay.game_fps,
                                        replay.game_length.seconds)


def convert_gametime_to_realtime(game_time_s, game_frames,
                                 game_fps, game_length_s):
    real_time = 0

    real_game_frame = game_time_s * game_fps
    real_fps = game_frames / game_length_s
    real_time = real_game_frame // real_fps

    return real_time


def convert_gametime_to_realtime_r(replay, game_time_s):
    return convert_gametime_to_realtime(game_time_s, replay.frames,
                                        replay.game_fps,
                                        replay.game_length.seconds)


def convert_frame_to_gametime(game_frame, game_fps):
    return game_frame // game_fps


def convert_frame_to_gametime_r(replay, game_frame):
    return convert_frame_to_gametime(game_frame, replay.game_fps)


def convert_frame_to_realtime_r(replay, game_frame):
    gt = convert_frame_to_gametime_r(replay, game_frame)
    return convert_gametime_to_realtime_r(replay, gt)


def is_hallucinated(unit):
    ################ bug : for whatever reason hallucinated attribute does not return correctly, it seems flags == 0 indicates hallucination (but only applies for army ########################
    return unit.hallucinated
    #return not ((unit.is_army and unit.flags != 0) or unit.is_worker)
