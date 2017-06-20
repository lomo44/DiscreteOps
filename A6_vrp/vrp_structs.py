class vrp_vehicle_list():
    def __init__(self, vehicle_count, vehicle_capacity):
        self.vehicle_count = vehicle_count
        self.vehicle_capacity = vehicle_capacity
        self.vehicle_schedule = []
        for index in range(vehicle_count):
            self.vehicle_schedule.append([])
    def get_vehicle_schedule(self, vehicle_index):
        return self.vehicle_schedule[vehicle_index]
        
class vrp_problem_context():
    def __init__(self):
        self.depot = None
        self.vehicle_list = None
        self.customers = None

