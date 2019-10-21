class FoodCount(object):
    """
    Container for tracking supply at a given second.
    
    Args:
        second (int): The second in the game.
        supply_used (int): The amount of supply used.
        supply_made (int): The amount of supply made from supply buildings.
        
    """

    def __init__(self, second, supply_used, supply_made):
        self.second = second
        self.supply_used = supply_used
        self.supply_made = supply_made


class BaseCount(object):
    """
    Container for the second a base was created in a game.
    
    Args:
        second (int): The second a base was created.
        
    """

    def __init__(self, second):
        self.second = second

        
class SupplyCount(object):
    """
    Container for the supply of a player at a specified 
    second in the game. Also includes the supply of the last unit
    created.
    
    Args:
        second (int): The second in the game.
        total_supply (int): The total supply used as this second
            in the game.
        unit_supply (int): The supply of the last unit made.
        is_worker (bool): Boolean that indicates whether the last
            unit made was a worker or not.
    
    """


    def __init__(self, second, total_supply, unit_supply, is_worker):
        self.second = second
        self.supply = total_supply
        self.unit_supply = unit_supply
        self.is_worker = is_worker
    

class ResourceCount(object):
    """
    Container for the resource collection rate and unspent at a specified
    second in the game.
    
    Args:
        second (int): The second in the game.
        res_col (int): The resource collection rate at this second in the game.
        res_unspent (int): The unspent resources at this second in the game.
        
    """

    def __init__(self, second, res_col, res_unspent):
        self.second = second
        self.res_col = res_col
        self.res_unspent = res_unspent

    def to_dict(self):
        return {"second": self.second,
                "res_col": self.res_col,
                "res_unspent": self.res_unspent
                }


class BuildOrderElement(object):

    def __init__(self, build_num, unit_name, total_supply, time, frame):
        self.build_num = build_num
        self.name = unit_name
        self.supply = total_supply
        self.time = time
        self.frame = frame
        
    def to_string(self):
        return "({0})|{1}|{2}|{3}s".format(self.build_num, self.name, self.supply, self.time)

    def __eq__(self, other):
        if isinstance(other, BuildOrderElement):
            return (self.build_num == other.build_num and
                    self.name == other.name and
                    self.supply == other.supply and
                    self.time == other.time and
                    self.frame == other.frame)
        else:
            return False

    def __str__(self):
        return self.to_string()


class BuildOrder(object):
        
    def __init__(self, name='', build=None):
        if build:
            self.build = build
        else:
            self.build = []
        self.name = name

    def serialize(self):
        serial = self.__dict__
        bld_s = []
        for bld in self.build:
            bld_s.append(bld.__dict__)
        serial['build'] = bld_s

        return serial
        
    def deserialize(self, json_obj):        
        self.__dict__ = json_obj
        blds = []
        for bld in self.build:
            blds.append(BuildOrderElement(bld['build_num'], bld['name'], bld['supply'], bld['time'], bld['frame']))
        self.__dict__['build'] = blds

    def __eq__(self, other):
        if isinstance(other, BuildOrder):
            if not self.name == other.name:
                return False
            if not len(self.build) == len(other.build):
                return False
            for x in range(len(self.build)):
                if not self.build[x] == other.build[x]:
                    return False
            return True
        else:
            return False

    def __str__(self):
        return self.name

        

class ReplayMetadata(object):

    def __init__(self):
        self.game_length = 0
        self.players = []
        self.player = []
        self.winner = ''
        self.date = ''

    def to_string(self):
        out_str = "{0} - {1}s - W:{2} - ".format(self.date, round(self.game_length, 1), self.winner)
        for pl in self.players[:-1]:
            out_str += "{0} vs ".format(pl)
        out_str += self.players[-1]

        return out_str

    def to_csv_list(self):
        out = []
        out.append(self.date)
        out.append(self.game_length)
        out.append(self.winner)
        pl_str = ""
        for pl in self.players[:-1]:
            pl_str += "{0} vs ".format(pl)
        pl_str += self.players[-1]
        out.append(pl_str)

        return out

    def csv_header():
        return ['Date', 'Length (s)', 'Winner', 'Players']
