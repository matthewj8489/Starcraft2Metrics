
WORKER_TAG = 'worker'
ARMY_TAG = 'army'
BUILDING_TAG = 'building'
UPGRADE_TAG = 'upgrade'
BASE_TAG = 'base'
SUPPLY_TAG = 'supply'
PRODUCTION_TAG = 'production'
TECH_TAG = 'tech'
STAT_TAG = 'stat'

Sc2UnitTags = {
    'Probe': [WORKER_TAG],
    'Nexus': [BUILDING_TAG, BASE_TAG],
    'Pylon': [BUILDING_TAG, SUPPLY_TAG],
    'Assimilator': [BUILDING_TAG],
    'Gateway': [BUILDING_TAG, PRODUCTION_TAG],
    'CyberneticsCore': [BUILDING_TAG, TECH_TAG],
    'Forge': [BUILDING_TAG, TECH_TAG],
    'PhotonCannon': [BUILDING_TAG],
    'ShieldBattery': [BUILDING_TAG],
    'RoboticsFacility': [BUILDING_TAG, PRODUCTION_TAG],
    'RoboticsBay': [BUILDING_TAG, TECH_TAG],
    'Stargate': [BUILDING_TAG, PRODUCTION_TAG],
    'FleetBeacon': [BUILDING_TAG, TECH_TAG],
    'TwilightCouncil': [BUILDING_TAG, TECH_TAG],
    'TemplarArchive': [BUILDING_TAG, TECH_TAG],
    'DarkShrine': [BUILDING_TAG, TECH_TAG],
    'ProtossGroundWeaponsLevel1': [UPGRADE_TAG, STAT_TAG], 'ProtossGroundWeaponsLevel2': [UPGRADE_TAG, STAT_TAG], 'ProtossGroundWeaponsLevel3': [UPGRADE_TAG, STAT_TAG],
    'ProtossGroundArmorsLevel1': [UPGRADE_TAG, STAT_TAG], 'ProtossGroundArmorsLevel2': [UPGRADE_TAG, STAT_TAG], 'ProtossGroundArmorsLevel3': [UPGRADE_TAG, STAT_TAG],
    'ProtossShieldsLevel1': [UPGRADE_TAG, STAT_TAG], 'ProtossShieldsLevel2': [UPGRADE_TAG, STAT_TAG], 'ProtossShieldsLevel3': [UPGRADE_TAG, STAT_TAG],
    'ProtossAirWeaponsLevel1': [UPGRADE_TAG, STAT_TAG], 'ProtossAirWeaponsLevel2': [UPGRADE_TAG, STAT_TAG], 'ProtossAirWeaponsLevel3': [UPGRADE_TAG, STAT_TAG],
    'ProtossAirArmorsLevel1': [UPGRADE_TAG, STAT_TAG], 'ProtossAirArmorsLevel2': [UPGRADE_TAG, STAT_TAG], 'ProtossAirArmorsLevel3': [UPGRADE_TAG, STAT_TAG],
    'Warp Gate': [UPGRADE_TAG, TECH_TAG],
    'Charge': [UPGRADE_TAG, TECH_TAG],
    'Blink': [UPGRADE_TAG, TECH_TAG],
    'Resonating Glaives': [UPGRADE_TAG, TECH_TAG],
    'Shadow Stride': [UPGRADE_TAG, TECH_TAG],
    'Psionic Storm': [UPGRADE_TAG, TECH_TAG],
    'Extended Thermal Lance': [UPGRADE_TAG, TECH_TAG],
    'Gravitic Drive': [UPGRADE_TAG, TECH_TAG],
    'Gravitic Boosters': [UPGRADE_TAG, TECH_TAG],
    'Anion Pulse-Crystals': [UPGRADE_TAG, TECH_TAG],
    'Zealot': [ARMY_TAG],
    'Stalker': [ARMY_TAG],
    'Sentry': [ARMY_TAG],
    'Adept': [ARMY_TAG],
    'HighTemplar': [ARMY_TAG],
    'DarkTemplar': [ARMY_TAG],
    'Archon': [ARMY_TAG],
    'Observer': [ARMY_TAG],
    'Immortal': [ARMY_TAG],
    'WarpPrism': [ARMY_TAG],
    'Disruptor': [ARMY_TAG],
    'Colossus': [ARMY_TAG],
    'Phoenix': [ARMY_TAG],
    'Oracle': [ARMY_TAG],
    'VoidRay': [ARMY_TAG],
    'Tempest': [ARMY_TAG],
    'Carrier': [ARMY_TAG],
    'Mothership': [ARMY_TAG]
}

def get_tags(unit_name):
    if unit_name in Sc2UnitTags:
        return Sc2UnitTags[unit_name]
    else:
        return []