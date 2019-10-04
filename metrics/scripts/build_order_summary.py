import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))
import argparse
from collections import Counter
from metric_factory.spawningtool_factory import SpawningtoolFactory

def is_base(boe):
    return boe.name in ['Nexus', 'CommandCenter', 'Hatchery']

def is_important_building(boe):
    return boe.name in ['Gateway', 'Forge', 'CyberneticsCore', 'PhotonCannon', 'RoboticsFacility', 'Stargate',
                       'TwilightCouncil', 'RoboticsBay', 'FleetBeacon', 'TemplarArchives', 'DarkShrine']

def generate_summary(bo):
    summary = []
    imp_bldgs = []

    for boe in bo:
        if is_base(boe):
            unique_bldgs = Counter(imp_bldgs)
            bldg_keys = list(unique_bldgs.keys())
            bldg_vals = list(unique_bldgs.values())
            new_str = ""
            for idx in range(len(unique_bldgs)):
                new_str += "{}x {} ".format(bldg_vals[idx], bldg_keys[idx])
            if new_str:
                summary.append(new_str)
            imp_bldgs.clear()
            summary.append("Expand")

        if is_important_building(boe):
            imp_bldgs.append(boe.name)

    return summary



def get_argument_parser():
    parser = argparse.ArgumentParser(description='Replay Build Order Summary')
    
    parser.add_argument('replay_path', type=str, help='replay file to extract build.')

    return parser


if __name__ == '__main__':

    parser = get_argument_parser()
    args = parser.parse_args()
    
    fact = SpawningtoolFactory(args.replay_path)

    meta = fact.generateReplayMetadata()

    for plyr in meta.player:
        print(plyr['name'])
        print("--------------")
        bo = fact.generateBuildOrderElements(plyr['name'])
        summary = generate_summary(bo)
        for elem in summary:
            print(elem)
        print("")
        
