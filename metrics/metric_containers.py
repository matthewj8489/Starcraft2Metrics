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


class ReplayMetadata(object):

    def __init__(self, game_length=0, players=[], winner='', date=''):
        self.game_length = game_length
        self.players = players
        self.winner = winner
        self.date = date


    def to_string(self):
        out_str = "{0} - {1}s - W:{2} - ".format(self.date, self.game_length, self.winner)
        for pl in self.players[:-1]:
            out_str += "{0} vs ".format(pl)
        out_str += self.players[-1]
        
