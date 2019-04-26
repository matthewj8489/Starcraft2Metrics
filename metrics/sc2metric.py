import math

import metrics.util


class Sc2MetricAnalyzer(object):
    """A class that derives useful metrics from replay files

    This class is an extension to the ``sc2reader`` player class. It is meant 
    to be used to offer useful metric data to each player in a Starcraft II replay. 
    The class contains raw data gathered from each replay to derive its metrics.
    The raw data is filled from the ``plugins`` associated with this package.

    Todo:
        - #TotalSupply : Total supply created by the player.
            (This is NOT current supply at given time)
        - #Workers : Total number of workers created by the player.
        - #Army : Total army supply created by the player.
        - #Upgrades : Total count of upgrades. (+1/2/3 weapons, psionic storm,
            charge, etc.)
        - TimeTo66Workers : Time at which the user created 66 workers
            (3-base saturation).
        - TimeTo75Workers : Time at which the user created 75 workers.
        - TimeTo3Bases : Time at which the 3 bases are finished.
        - TimeTo4Bases : Time at which the 4 bases are finished.
        - TimeToMax : Time at which the total supply created is 199 or above
            (stops counting workers above 75)
        - SupplyCapped : Time spent supply blocked.
        - #SupplyCreateRate : Average rate at which supply buildings are
            created until 200 supply
        - AvgAPM : Average APM
        - #AvgEPM : Average EPM
        - #AvgSPM : Average SPM
        - #AvgMacroCycleTime : Average time spent issuing macro commands
            (vs army commands) (or maybe the avg time between giving a worker a
            command and issuing another command not to the worker)
        - #AvgHarassDeflection : A score that rates the player's ability
            to deflect and minimize damage incurred from harassment attacks.
            (works off of minerals/probes/tech/mining time lost?)
        - #IdleBaseTime66 : Total time town halls are idle (not making workers) before 66 workers
        - #IdleBaseTime75 : Total time town halls are idle (not making workers) before 75 workers
        - AvgSQ : Spending Quotient. SQ(i,u)=35(0.00137i-ln(u))+240,
            where i=resource collection rate, u=average unspent resources
        - AvgSQPreMax : Spending Quotient before maxed out.
        - AvgUnspent : Average unspent resources during the game.
        - AvgUnspentPreMax : Average unspent resources before maxed out.
        - AvgColRate : Average resource collection rate during the game.
        - AvgColRatePreMax : Average resource collection rate before maxed out.
        - #Units : Dictionary of all the units created, keyed by the units'
            names.
        - #PPM : average(mean) PAC per minute
        - #PAL : PAC action latency. e.g.: how long it takes you to take your
            first action after each fixation shift. (mean average)
        - #APP : Actions per PAC. The average(mean) number of actions you
            take each PAC
        - #GAP : How long it takes you, after finishing your actions in
            one PAC to establish a new fixaction. (mean average)
    
    """

    
    def __init__(self):
        """Initialization of the class"""
        
        #: A list of :class:`~metrics.metric_containers.SupplyCount` for each army supply created.
        self.army_created = []

        #: A list of :class:`~metrics.metric_containers.SupplyCount` for each worker created.
        self.workers_created = []

        #: A list of :class:`~metrics.metric_containers.SupplyCount` for each unit created.
        self.supply_created = []

        #: A list of :class:`~metrics.metric_containers.BaseCount` for each base created.
        self.bases_created = []

        #: A list of :class:`~metrics.metric_containers.FoodCount` for each unit created.
        self.current_food_used = []
        
        #: A list of :class:`~metrics.metric_containers.FoodCount` for each supply provider building.
        self.current_food_made = []
        
        #: A list of :class:`~metrics.metric_containers.FoodCount` for each unit and supply provider
        #: created.
        self.supply = []
        
        #: A list of :class:`~metrics.metric_containers.ResourceCount` for resources collected and 
        #: resources unspent every 10 seconds.
        self.resources = []
        
        #: The player's average apm
        self.avg_apm = 0
        

    def metrics(self):
        """A dictionairy of basic metrics."""
        return {'TimeToMax' : self.time_to_supply_created_max_workers(198, 75),
                'TimeTo3Bases' : self.time_to_bases_created(3),
                'TimeTo4Bases' : self.time_to_bases_created(4),
                'TimeTo66Workers' : self.time_to_workers_created(66),
                'TimeTo75Workers' : self.time_to_workers_created(75),
                'AvgAPM' : self.avg_apm,
                'AvgSQ' : self.avg_sq(),
                'AvgSQPreMax' : self.avg_sq_pre_max(),
                'AvgUnspent' : self.aur(),
                'AvgUnspentPreMax' : self.aur_pre_max(),
                'AvgColRate' : self.avg_rcr(),
                'AvgColRatePreMax' : self.avg_rcr_pre_max(),
                'SupplyCapped' : self.supply_capped()
               }             
        

    def first_max(self):
        """Returns the time at which the player first reached max supply."""
        return next((fd.second for fd in self.current_food_used
                     if fd.supply >= 200), -1)


    def _sq(self, resources):
        sum_res_col_rate = 0
        sum_unspent_res = 0
        for res in resources:
            sum_res_col_rate += res.res_col
            sum_unspent_res += res.res_unspent

        avg_col_rate = sum_res_col_rate / len(resources)
        avg_unspent = sum_unspent_res / len(resources)

        # SQ(i,u)=35(0.00137i-ln(u))+240, where i=resource collection rate,
        #   u=average unspent resources
        sq = 35 * (0.00137 * avg_col_rate - math.log(avg_unspent)) + 240
                
        return sq


    def avg_sq(self):
        """Average Spending Quotient

        Calculates the average Spending Quotient (SQ).

        Returns:
            int: The average Spending Quotient (SQ).
            
        """
        return self._sq(self.resources)


    def avg_sq_at_time(self, time_s):
        """Average Spending Quotient up to a specified time

        Calculates the average Spending Quotient (SQ) up until the specified
        time.

        Args:
            time_s (int): The time in the replay to stop calculating spending
                quotient.

        Returns:
            int: The average Spending Quotient (SQ) up until the specified time.
            
        """
        resources = list(filter(lambda res: res.second <= time_s,
                                self.resources))

        if len(resources) > 0:
            return self._sq(resources)
        else:
            return 0


    def avg_sq_pre_max(self):
        """Average Spending Quotient before max supply

        Calculates the average Spending Quotient (SQ) up until the player first
        reaches max supply.

        Returns:
            int: The average Spending Quotient (SQ) up until the player first
                maxes.
            
        """
        max_s = self.first_max()

        if max_s >= 0:
            return self.avg_sq_at_time(max_s)
        else:
            return self.avg_sq()
        

    def _aur(self, resources):
        if len(resources) > 0:
            sum_aur = 0
            for res in resources:
                sum_aur += res.res_unspent

            return sum_aur / len(resources)


    def aur(self):
        """Average Unspent Resources

        Calculates the Average Unspent Resources (AUR) during the game.

        Returns:
            int: The Average Unspent Resources (AUR)
            
        """
        return self._aur(self.resources)


    def aur_at_time(self, time_s):
        """Averague Unspent Resources up to a specified time

        Calculates the Average Unspent Resources (AUR) up until the specified
        time.

        Args:
            time_s (int): The time in the replay to stop calculating average
                unspent resources.

        Returns:
            int: The Average Unspent Resources (AUR) up until the specified
                time.
            
        """
        resources = list(filter(lambda res: res.second <= time_s,
                                self.resources))

        return self._aur(resources)


    def aur_pre_max(self):
        """Average Unspent Resources before max supply

        Calculates the Average Unspent Resources (AUR) up until the player first
        reaches max supply.

        Returns:
            int: The Average Unspent Resources (AUR) up until the player first
                maxes.
            
        """
        max_s = self.first_max()

        if max_s >= 0:
            return self.aur_at_time(max_s)
        else:
            return self.aur()


    def _avg_rcr(self, resources):
        if len(resources) > 0:
            sum_rcr = 0
            for res in resources:
                sum_rcr += res.res_col

            return sum_rcr / len(resources)


    def avg_rcr(self):
        """Average Resource Collection Rate

        Calculates the average Resource Collection Rate (RCR) during the game.

        Returns:
            int: The average Resource Collection Rate (RCR)
            
        """
        return self._avg_rcr(self.resources)


    def avg_rcr_at_time(self, time_s):
        """Average Resource Collection Rate up to a specified time

        Calculates the average Resource Collection Rate (RCR) up until the
        specified time.

        Args:
            time_s (int): The time in the replay to stop calculating average
                resource collection rate.

        Returns:
            int: The average Resource Collection Rate (RCR) up until the
                specified time.
            
        """
        resources = list(filter(lambda res: res.second <= time_s,
                                self.resources))

        return self._avg_rcr(resources)


    def avg_rcr_pre_max(self):
        """Average Resource Collection Rate before max supply

        Calculates the average Resource Collection Rate (RCR) up until the
        player first reaches max supply.

        Returns:
            int: The average Resource Collection Rate (RCR) up until the player
                first maxes.
            
        """
        max_s = self.first_max()

        if max_s >= 0:
            return self.avg_rcr_at_time(max_s)
        else:
            return self.avg_rcr()
            

    def supply_capped(self):
        """Time spent supply capped

        Determines the amount of time the player was supply capped this game.
        Supply capped is acknowledged when supply of units = supply created
        when supply created < 200.

        Returns:
            int: The amount of time spent supply capped.
            
        """        
        
        supply_blocked = False
        time_of_supply_block = 0
        sc = 0
        for sp in self.supply:
            if (supply_blocked == False and
                sp.supply_used >= sp.supply_made and
                sp.supply_made < 200):
                supply_blocked = True
                time_of_supply_block = sp.second
            elif (supply_blocked == True and
                  (sp.supply_used < sp.supply_made or
                  sp.supply_made >= 200)):
                sc += (sp.second - time_of_supply_block)
                supply_blocked = False
                time_of_supply_block = 0
                
        return sc
            

    def workers_created_at_time(self, time_s):
        """Number of workers created up to the specified time

        Determines the total number of workers created at the specified time.
        This function is accumulative and does not handle workers lost.

        Args:
            time_s (int): The time (in seconds) of the replay to count workers.

        Returns:
            int: The number of workers created.
            
        """
        workers = 0
        idx = 0
        while (len(self.workers_created) > idx
               and self.workers_created[idx].second < time_s):
            workers += 1
            idx += 1

        return workers


    def army_created_at_time(self, game_time_s):
        """The army supply created up to a specified time

        Calculate the total army supply created at the specified time.

        Args:
            game_time_s (int): The time (in seconds) of the replay to count army
                supply.

        Returns:
            int: The amount of army supply created in the given time.
            
        """
        idx = 0
        while (len(self.army_created) > idx
               and self.army_created[idx].second <= game_time_s):
            idx += 1

        return self.army_created[idx-1].supply


    def supply_created_at_time(self, real_time_s):
        """The total supply created up to a specified time

        Calculate the total supply created at the specified time.

        Args:
            real_time_s (int): The time (in seconds) of the replay to count
                supply.

        Returns:
            int: The amount of supply created in the given time.
            
        """
        supply = 0
        supply += self.workers_created_at_time(real_time_s)
        supply += self.army_created_at_time(real_time_s)

        return supply


    def time_to_workers_created(self, worker_count):
        """The time at which the number of workers had been created

        Finds the time that the specified number of workers have been created.
        This does not account for loss of workers.

        Args:
            worker_count (int): The number of workers to find the time created.

        Returns:
            int: The time at which the total number of workers were created.
            
        """
        if worker_count <= len(self.workers_created):
            return self.workers_created[worker_count-1].second
        else:
            return None


    def time_to_supply_created(self, supply_count):
        """The time at which the specified supply had been created

        Finds the time when the specified supply was created. This does not
        take into account supply lost.
        
        Args:
            supply_count (int): The supply desired.

        Returns:
            int: The time when the supply was created in the replay.
            
        """
        supp = list(filter(lambda sp: sp.supply <= supply_count,
                           self.supply_created))

        if len(supp) > 0:
            return supp[len(supp)-1].second
        else:
            return None
        

    def time_to_supply_created_max_workers(self, supply_count,
                                           max_workers_counted):
        """The time at which the specified supply had been created

        Finds the time when the specified supply was reached, but only counts a specified
        number of workers towards that supply created count. This does not take into
        account supply lost.

        Args:
            supply_count (int): The supply desired.
            max_workers_counted (int): The maximum number of workers to count
                towards the supply created.

        Returns:
            int: The time when the supply was created in the replay.
            
        """
        supp = 0
        workers = 0
        for sc in self.supply_created:
            if not sc.is_worker or workers < max_workers_counted:
                supp += sc.unit_supply
                if supp >= supply_count:
                    return sc.second
                if sc.is_worker:
                    workers += 1

        return None


    def time_to_bases_created(self, base_count):
        """The time at which the number of bases had been created

        Finds the time when the specified number of bases has been reached.
        This does not take into account any bases lost.

        Args:
            base_count (int): The number of bases desired.

        Returns:
            int: The time when the number of bases had been created.
            
        """
        if base_count <= len(self.bases_created) and base_count > 0:
            return self.bases_created[base_count-1].second
        else:
            return None   
        

##    def units_created(self, real_time_s):
##        if not 'UnitBornEvent' in self._events or not 'UnitInitEvent' in self._events:
##            return 0
##        units_created = {"Probe": 0, "Zealot": 0, "Sentry": 0, "Stalker": 0, "Adept": 0, "HighTemplar": 0,
##                         "DarkTemplar": 0, "Archon": 0, "Observer": 0, "Immortal": 0, "Colossus": 0,
##                         "Disruptor": 0, "Phoenix": 0, "Oracle": 0, "VoidRay": 0, "Carrier": 0, "Tempest": 0}
##
##        unit_born_events = self._events['UnitBornEvent']
##        unit_init_events = self._events['UnitInitEvent']
##        game_time_s = util.convert_realtime_to_gametime_r(self._replay, real_time_s)
##        
##        player_ube = list(filter(lambda ube: ube.control_pid == self._player_id, unit_born_events))
##        player_uie = list(filter(lambda uie: uie.control_pid == self._player_id, unit_init_events))
##
##        for ube in player_ube:
##            if (ube.second <= game_time_s) and (ube.unit.name in units_created) and (not self._isHallucinated(ube.unit)):
##                units_created[ube.unit.name] += 1
##
##        for uie in player_uie:
##            if (uie.second <= game_time_s) and (uie.unit.name in units_created) and (not self._isHallucinated(uie.unit)):
##                units_created[uie.unit.name] += 1
##
##        return units_created

##    def encode_json(self):
##        if isinstance(self, Sc2MetricAnalyzer):
##            res_dict = {'__ResourceCount__': True}
##            for res in self.resources:
##                res_dict.update(res.to_dict())
##
##
##            
##            return {'__Sc2MetricAnalyzer__': True,
##                    'army_created': self.army_created,
##                    'workers_created': self.workers_created,
##                    'supply_created': self.supply_created,
##                    'bases_created': self.bases_created,
##                    'current_food_used': self.current_food_used,
##                    'current_food_made': self.current_food_made,
##                    'resources': self.resources,
##                    'avg_apm': self.avg_apm
##                    }
##        else:
##            type_name = z.__class__.__name__
##            raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

    

   
########## Testing ###########
if __name__ == '__main__':

    ma = Sc2MetricAnalyzer("..\\test\\test_replays\\Year Zero LE (9).SC2Replay",
                           1)
