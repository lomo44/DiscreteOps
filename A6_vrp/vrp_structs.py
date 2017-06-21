
class vrp_solution():
    def __init__(self, vehicle_count, vehicle_capacity):
        self.vehicle_count = vehicle_count
        self.vehicle_capacity = vehicle_capacity
        self.vehicle_schedule = []
        self.current_capacity = []
        self.current_cost = 0
        for index in range(vehicle_count):
            self.vehicle_schedule.append([])
    def get_vehicle_schedule(self, vehicle_index):
        return self.vehicle_schedule[vehicle_index]
    def get_schedule_capacity(self,start_index, end_index, vehicle_index, customers):
        return sum(customers[self.vehicle_schedule[vehicle_index][i]].demand for i in range(start_index, end_index))
    def get_schedule_cost(self, start_index, end_index,vehicle_index, problem_cache):
        if start_index == end_index:
            return 0
        else:
            return_cost = 0
            for index in range(0,len(self.vehicle_schedule[vehicle_index])):
                return_cost += problem_cache.get_distance_between_customers(self.vehicle_schedule[vehicle_index][index],\
                self.vehicle_schedule[vehicle_index][index+1])
            return return_cost
        
class vrp_problem_context():
    def __init__(self):
        self.depot = None
        self.vehicle_list = None
        self.customers = None
    


