
class Facility:
    def __init__(self):
        self.index = 0
        self.setup_cost = 0
        self.capacity = 0
        self.location = None

class Customer:
    def __init__(self):
        self.index = 0
        self.demand = 0
        self.assigned_facility = 0
        self.location = None