from vrp_cache import vrp_cache

class vrp_solution():
    def __init__(self, vehicle_count, vehicle_capacity):
        self.vehicle_count = vehicle_count
        self.vehicle_capacity = vehicle_capacity
        self.vehicle_schedule = []
        self.current_capacity = []
        self.current_cost = 0
        for index in range(vehicle_count):
            self.vehicle_schedule.append([0])
            self.current_capacity.append(self.vehicle_capacity)
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
    def get_remove_delta(self, vehicle_index, customer_position_index, problem_cache:vrp_cache):
        schedule = self.vehicle_schedule[vehicle_index]
        schedule_size = len(schedule)
        return_cost = 0
        return_cost -= problem_cache.get_distance_between_customers(schedule[customer_position_index], schedule[(customer_position_index + 1) % schedule_size])
        return_cost -= problem_cache.get_distance_between_customers(schedule[customer_position_index], schedule[(customer_position_index - 1) % schedule_size])
        return_cost += problem_cache.get_distance_between_customers(schedule[(customer_position_index + 1) % schedule_size],
                                                                    schedule[(customer_position_index - 1) % schedule_size])
        return  return_cost
    def get_insert_delta(self, vehicle_index, customer_index, insert_position, problem_cache:vrp_cache):
        schedule = self.vehicle_schedule[vehicle_index]
        schedule_size = len(schedule)
        return_cost = 0
        return_cost -= problem_cache.get_distance_between_customers(schedule[insert_position % schedule_size], schedule[(insert_position - 1) % schedule_size])
        return_cost += problem_cache.get_distance_between_customers(customer_index,schedule[insert_position % schedule_size])
        return_cost += problem_cache.get_distance_between_customers(customer_index,schedule[(insert_position - 1) % schedule_size])
        return return_cost

    def format_schedule(self):
        for schedule in self.vehicle_schedule:
            while schedule[0] != 0:
                schedule.append(schedule.pop(0))
    def generate_output_string(self):
        self.format_schedule()
        outputData = '%.2f' % self.current_cost + ' ' + str(0) + '\n'
        for v in self.vehicle_schedule:
            outputData += ' '.join(map(lambda x: str(x), v))
            outputData += ' ' + '0' + '\n'
        return outputData
class vrp_problem_context():
    def __init__(self):
        self.depot = None
        self.vehicle_count = None
        self.vehicle_max_capacity = None
        self.customers = None

    


