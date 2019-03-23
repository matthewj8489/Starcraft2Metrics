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
    

class ResourceCount(object):

    def __init__(self, second, res_col, res_unspent):
        self.second = second
        self.res_col = res_col
        self.res_unspent = res_unspent
