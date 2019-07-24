import mpyq
import json
from s2protocol import versions

import pprint



archive = mpyq.MPQArchive('../tests/integration/test_replays/pvt_macro1.SC2Replay')
contents = archive.header['user_data_header']['content']

header = versions.latest().decode_replay_header(contents)
baseBuild = header['m_version']['m_baseBuild']
protocol = versions.build(baseBuild)
contents = archive.read_file('replay.gamemetadata.json')


metadata = json.loads(contents)
pprint.pprint(metadata)


contents = archive.read_file('replay.game.events')
game_events = protocol.decode_replay_game_events(contents)


cam_upd_evt = list(filter(lambda x: x['_event'] == 'NNet.Game.SCameraUpdateEvent' and x['_userid']['m_userId'] == 0, game_events))


contents = archive.read_file('replay.details')
details = protocol.decode_replay_details(contents)

contents = archive.read_file('replay.details.backup')
details_backup = protocol.decode_replay_details(contents)

contents = archive.read_file('replay.initData')
initData = protocol.decode_replay_initdata(contents)

contents = archive.read_file('replay.attributes.events')
attributes = protocol.decode_replay_attributes_events(contents)


if hasattr(protocol, 'decode_replay_tracker_events'):
    contents = archive.read_file('replay.tracker.events')
    tracker_events = protocol.decode_replay_tracker_events(contents)
    
stats_events = list(filter(lambda x: x['_event'] == 'NNet.Replay.Tracker.SPlayerStatsEvent' and x['m_playerId'] == 1, tracker_events))
