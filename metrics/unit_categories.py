
WORKER_TAG = 'worker'
ARMY_TAG = 'army'
BUILDING_TAG = 'building'
UPGRADE_TAG = 'upgrade'
BASE_TAG = 'base'
SUPPLY_TAG = 'supply'
PRODUCTION_TAG = 'production'
TECH_TAG = 'tech'
STAT_TAG = 'stat'

Sc2UnitCategories = {
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
    'RoboticsSupportBay': [BUILDING_TAG, TECH_TAG],
    'Stargate': [BUILDING_TAG, PRODUCTION_TAG],
    'FleetBeacon': [BUILDING_TAG, TECH_TAG],
    'TwilightCouncil': [BUILDING_TAG, TECH_TAG],
    'TemplarArchives': [BUILDING_TAG, TECH_TAG],
    'DarkShrine': [BUILDING_TAG, TECH_TAG],
    'ProtossGroundWeapons1': [UPGRADE_TAG, STAT_TAG], 'ProtossGroundWeapons2': [UPGRADE_TAG, STAT_TAG], 'ProtossGroundWeapons3': [UPGRADE_TAG, STAT_TAG],
    'ProtossGroundArmor1': [UPGRADE_TAG, STAT_TAG], 'ProtossGroundArmor2': [UPGRADE_TAG, STAT_TAG], 'ProtossGroundArmor3': [UPGRADE_TAG, STAT_TAG],
    'ProtossShieldArmor1': [UPGRADE_TAG, STAT_TAG], 'ProtossShieldArmor2': [UPGRADE_TAG, STAT_TAG], 'ProtossShieldArmor3': [UPGRADE_TAG, STAT_TAG],
    'ProtossAirWeapons1': [UPGRADE_TAG, STAT_TAG], 'ProtossAirWeapons2': [UPGRADE_TAG, STAT_TAG], 'ProtossAirWeapons3': [UPGRADE_TAG, STAT_TAG],
    'ProtossAirArmor1': [UPGRADE_TAG, STAT_TAG], 'ProtossAirArmor2': [UPGRADE_TAG, STAT_TAG], 'ProtossAirArmor3': [UPGRADE_TAG, STAT_TAG],
    'WarpGate': [UPGRADE_TAG, TECH_TAG],
    'Charge': [UPGRADE_TAG, TECH_TAG],
    'Blink': [UPGRADE_TAG, TECH_TAG],
    'ResonatingGlaives': [UPGRADE_TAG, TECH_TAG],
    'ShadowStride': [UPGRADE_TAG, TECH_TAG],
    'PsionicStorm': [UPGRADE_TAG, TECH_TAG],
    'ExtendedThermalLance': [UPGRADE_TAG, TECH_TAG],
    'GraviticDrive': [UPGRADE_TAG, TECH_TAG],
    'GraviticBoosters': [UPGRADE_TAG, TECH_TAG],
    'AnionPulseCrystals': [UPGRADE_TAG, TECH_TAG],
    'Zealot': [ARMY_TAG],
    'Stalker': [ARMY_TAG],
    'Sentry': [ARMY_TAG],
    'Adept': [ARMY_TAG],
    'HighTemplar': [ARMY_TAG],
    'DarkTemplar': [ARMY_TAG],
    'Archon': [ARMY_TAG],
    'Observer': [ARMY_TAG],
    'Immortal': [ARMY_TAG],
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
    if unit_name in Sc2UnitCategories:
        return Sc2UnitCategories[unit_name]
    else:
        return []