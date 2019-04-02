class FoodCount(object):
    """
    Container for tracking supply at a given second.
    
    Args:
        second (int): The second in the game.
        supply (int): The supply amount.
        
    """

    def __init__(self, second, supply):
        self.second = second
        self.supply = supply


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
    Container for the resources collected and unspent at a specified
    second in the game.
    
    Args:
        second (int): The second in the game.
        res_col (int): The resources collected at this second in the game.
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
