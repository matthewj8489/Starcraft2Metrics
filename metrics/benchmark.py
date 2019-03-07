import sc2reader
from sc2reader.engine.plugins import APMTracker
sc2reader.engine.register_plugin(APMTracker())
import util
import math

class Benchmark(object):
    '''
    Find benchmark metrics for the given replay file at the given real time.
    (Benchmarks include 'Total Supply Created', 'Workers Created', 'Army Created')

    Keyword arguments:
    replay_file -- the location of the replay to parse.
    player_id -- the id number of the player to monitor in the replay
    benchmark_time_s -- the real time of when to take the benchmark measurement

    Output:
    Dictionary containing the following keys:
    'TotalSupply' : Total supply created by the player. (This is NOT current supply at given time)
    'Workers' : Total number of workers created by the player.
    'Army' : Total army supply created by the player.
    'Upgrades' : Total count of upgrades. (+1/2/3 weapons, psionic storm, charge, etc.)
    'TimeTo66Workers' : Time at which the user created 66 workers (3-base saturation).
    'TimeTo75Workers' : Time at which the user created 75 workers.
    'TimeTo3Bases' : Time at which the 3 bases are finished.
    'TimeTo4Bases' : Time at which the 4 bases are finished.
    'TimeToMax' : Time at which the total supply created is 199 or above (stops counting workers above 75)
    'SupplyBlocked' : Time spent supply blocked.
    'SupplyCreateRate' : Average rate at which supply buildings are created until 200 supply
    'AvgAPM' : Average APM
    'AvgEPM' : Average EPM
    'AvgSPM' : Average SPM
    'AvgMacroCycleTime : Average time spent issuing macro commands (vs army commands) (or maybe the avg time between giving a worker a command and issuing another command not to the worker)
    'AvgHarassDeflection' : A score that rates the player's ability to deflect and minimize damage incurred from harassment attacks. (works off of minerals/probes/tech/mining time lost?)
    'IdleBaseTime66' : Total time town halls are idle (not making workers) before 66 workers
    'IdleBaseTime75' : Total time town halls are idle (not making workers) before 75 workers
    'AvgSQ' : Spending Quotient. SQ(i,u)=35(0.00137i-ln(u))+240, where i=resource collection rate, u=average unspent resources
    'AvgSQPreMax' : Spending Quotient before maxed out.
    'Units' : Dictionary of all the units created, keyed by the units' names.
    'PPM' : average(mean) PAC per minute
    'PAL' : PAC action latency. e.g.: how long it takes you to take your first action after each fixation shift. (mean average)
    'APP' : Actions per PAC. The average(mean) number of actions you take each PAC
    'GAP' : How long it takes you, after finishing your actions in one PAC to establish a new fixaction. (mean average)
    '''   

    
    def __init__(self, replay_file, player_id):       
        #: Replay structure
        self._replay = sc2reader.load_replay(replay_file)

        #: An events dictionary from the replay
        event_names = set([event.name for event in self._replay.events])
        self._events = {name: [] for name in event_names}
        for event in self._replay.events:
            self._events[event.name].append(event)
         
        #: The ID of the player for whom to parse benchmark data
        self._player_id = player_id


    def benchmarks(self):
        return {'TimeToMax' : self.time_to_supply_count_created_excluding_extra_workers(198, 75),
                'TimeTo3Bases' : self.time_to_total_bases(3),
                'TimeTo4Bases' : self.time_to_total_bases(4),
                'TimeTo66Workers' : self.time_to_worker_count(66),
                'TimeTo75Workers' : self.time_to_worker_count(75),
                'AvgAPM' : self.avg_apm(),
                'AvgSQ' : self.avg_sq(),
                'AvgSQPreMax' : self.avg_sq_pre_max()
               }             
        

    def avg_apm(self):
        return self._replay.player[self._player_id].avg_apm / util.gametime_to_realtime_constant_r(self._replay)


    def sq(self, player_stats_events):
        sum_res_col_rate = 0
        sum_unspent_res = 0
        for pse in player_stats_events:
            sum_res_col_rate += (pse.minerals_collection_rate + pse.vespene_collection_rate)
            sum_unspent_res += (pse.minerals_current + pse.vespene_current)

        avg_col_rate = sum_res_col_rate / len(player_stats_events)
        avg_unspent = sum_unspent_res / len(player_stats_events)

        # SQ(i,u)=35(0.00137i-ln(u))+240, where i=resource collection rate, u=average unspent resources
        sq = 35 * (0.00137 * avg_col_rate - math.log(avg_unspent)) + 240
                
        return sq
    

    def avg_sq_at_time(self, time_s):
        player_stats_events = list(filter(lambda pse: pse.pid == self._player_id, self._events['PlayerStatsEvent']))
        pse_at_time = list()

        idx = 0
        while (idx < len(player_stats_events) and player_stats_events[idx].second <= time_s):
            pse_at_time.append(player_stats_events[idx])
            idx += 1
            
        return self.sq(pse_at_time)


    def avg_sq(self):
        player_stats_events = list(filter(lambda pse: pse.pid == self._player_id, self._events['PlayerStatsEvent']))
                       
        return self.sq(player_stats_events)


    def avg_sq_pre_max(self):
        player_stats_events = list(filter(lambda pse: pse.pid == self._player_id, self._events['PlayerStatsEvent']))
        pse_premax = list()

        idx = 0
        while (idx < len(player_stats_events) and player_stats_events[idx].food_used <= 198):
            pse_premax.append(player_stats_events[idx])
            idx += 1
        
        return self.sq(pse_premax)


    def workers_created(self, real_time_s):
        units = list(filter(lambda ut: ut.owner.pid == self._player_id and ut.is_worker and (ut.hallucinated == False), self._replay.player[self._player_id].units))
        game_time_s = util.convert_realtime_to_gametime_r(self._replay, real_time_s)
        units_r = sorted(units, key=lambda ut: ut.finished_at)

        worker_count = 0
        for ut in units_r:
            if util.convert_frame_to_gametime_r(self._replay, ut.finished_at) <= game_time_s:
                worker_count += 1

        return worker_count


    def army_created(self, real_time_s):
        if not 'UnitBornEvent' in self._events or not 'UnitInitEvent' in self._events:
            return 0
        unit_born_events = self._events['UnitBornEvent']
        unit_init_events = self._events['UnitInitEvent']   
        army_supply_count = 0
        game_time_s = util.convert_realtime_to_gametime_r(self._replay, real_time_s)

        player_ube = list(filter(lambda ube: ube.control_pid == self._player_id, unit_born_events))
        player_army_ube = list(filter(lambda ube: ube.unit.is_army, player_ube))

        for ube in player_army_ube:
            if (ube.second <= game_time_s) and (ube.unit.name != "Archon") and (not ube.unit.hallucinated):
                army_supply_count += ube.unit.supply

        player_uie = list(filter(lambda uie: uie.control_pid == self._player_id, unit_init_events))
        player_army_uie = list(filter(lambda uie: uie.unit.is_army, player_uie))

        for uie in player_army_uie:
            if (uie.second <= game_time_s) and (uie.unit.name != "Archon") and (not uie.unit.hallucinated):
                army_supply_count += uie.unit.supply

        return army_supply_count


    def total_supply_created(self, real_time_s):
        supply = 0
        supply += self.workers_created(real_time_s)
        supply += self.army_created(real_time_s)

        return supply


    def time_to_worker_count(self, worker_count):
        units = list(filter(lambda ut: ut.owner.pid == self._player_id and ut.is_worker and (ut.hallucinated == False), self._replay.player[self._player_id].units))

        if worker_count <= len(units):
            return util.convert_frame_to_realtime_r(self._replay, units[worker_count - 1].finished_at)
        else:
            return -1


    def time_to_supply_count_created(self, supply_count):
        # filter all of the player units into just the workers + army that were not hallucinated
        units = list(filter(lambda ut: ut.owner.pid == self._player_id and (ut.is_army or ut.is_worker) and (ut.hallucinated == False), self._replay.player[self._player_id].units))

        # filter out special cases, such as Archons that were morphed from templars
        units_r = list(filter(lambda ut: ut.name != "Archon", units))
              
        supp = 0
        for ut in units_r:
            supp += ut.supply
            if supp >= supply_count:
                return util.convert_frame_to_realtime_r(self._replay, ut.finished_at)

        return -1


    def time_to_supply_count_created_excluding_extra_workers(self, supply_count, max_workers_counted):
        units = list(filter(lambda ut: ut.owner.pid == self._player_id and (ut.is_army or ut.is_worker) and (ut.hallucinated == False), self._replay.player[self._player_id].units))
        units_r = list(filter(lambda ut: ut.name != "Archon", units))
        
        supp = 0
        workers = 0
        for ut in units_r:
            if not ut.is_worker or workers < max_workers_counted:
                supp += ut.supply
                if supp >= supply_count:
                    return util.convert_frame_to_realtime_r(self._replay, ut.finished_at)
                if ut.is_worker:
                    workers += 1

        return -1

    def time_to_total_bases(self, total_bases):
        bases = list(filter(lambda ut: ut.name == 'Nexus' and ut.finished_at is not None, self._replay.player[self._player_id].units))
        bases_r = sorted(bases, key=lambda ut: ut.finished_at)

        if total_bases <= len(bases_r):
            return util.convert_frame_to_realtime_r(self._replay, bases_r[total_bases - 1].finished_at)
        else:
            return -1       
        

    def units_created(self, real_time_s):
        if not 'UnitBornEvent' in self._events or not 'UnitInitEvent' in self._events:
            return 0
        units_created = {"Probe": 0, "Zealot": 0, "Sentry": 0, "Stalker": 0, "Adept": 0, "HighTemplar": 0,
                         "DarkTemplar": 0, "Archon": 0, "Observer": 0, "Immortal": 0, "Colossus": 0,
                         "Disruptor": 0, "Phoenix": 0, "Oracle": 0, "VoidRay": 0, "Carrier": 0, "Tempest": 0}

        unit_born_events = self._events['UnitBornEvent']
        unit_init_events = self._events['UnitInitEvent']
        game_time_s = util.convert_realtime_to_gametime_r(self._replay, real_time_s)
        
        player_ube = list(filter(lambda ube: ube.control_pid == self._player_id, unit_born_events))
        player_uie = list(filter(lambda uie: uie.control_pid == self._player_id, unit_init_events))

        for ube in player_ube:
            if (ube.second <= game_time_s) and (ube.unit.name in units_created) and (ube.unit.hallucinated == False):
                units_created[ube.unit.name] += 1

        for uie in player_uie:
            if (uie.second <= game_time_s) and (uie.unit.name in units_created) and (uie.unit.hallucinated == False):
                units_created[uie.unit.name] += 1

        return units_created



   
########## Testing ###########
if __name__ == '__main__':

    bc = Benchmark("..\\test\\test_replays\\Year Zero LE (9).SC2Replay", 1)
