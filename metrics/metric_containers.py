class FoodCount(object):

    def __init__(self, second, supply):
        self.second = second
        self.supply = supply


class BaseCount(object):

    def __init__(self, second):
        self.second = second

        
class SupplyCount(object):

    def __init__(self, second, total_supply, unit_supply, is_worker):
        self.second = second
        self.supply = total_supply
        self.unit_supply = unit_supply
        self.is_worker = is_worker
    
