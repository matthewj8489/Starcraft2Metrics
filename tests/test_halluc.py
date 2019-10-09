import sc2reader

class TestHallucinate(unittest.TestCase):

    def test_hallucinated_units(self):
        rep = sc2reader.load_replay("test_replays\sentry_hallucinate.SC2Replay")
        

if __name__ == '__main__':
