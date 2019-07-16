

class BuildOrderDeviation(object):

    def __init__(self):
        
        self.deviation = None
        self.bo_discrepancy = [] # {'name' : '', 'sup_dif' : 0, 'time_dif' : 0}
        self.worst_deviation = None


    def calculate_deviation(golden_bo, compare_bo):
        self.deviation = None
        self.bo_discrepancy = []
        self.worst_deviation = None
        return self.deviation


    def detect_build_order(golden_bo, compare_bo):
        confidence = 0
        deviation = calculate_deviation(golden_bo, compare_bo)

        return [confidence, deviation]


if __name__ == '__main__':
    bod = BuildOrderDeviation()
    
