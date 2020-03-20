import numpy as np
import pandas as pd

class Heuristic():

    def __init__(self, clients, params):
        self.clients = clients
        self.velocity = params["velocity"]
        self.service_time = params["service_time"]
        self.vehicle_capacity = params["vehicle_capacity"]
        self.routes = pd.DataFrame(columns=["num_clients", "instants", "route_plan", "inventory"])

    def heurisitc_algo(self):
        create_route = True
        self.get_dist_matrix()
        self.get_time_matrix()
        ordered_clients = self.clients.copy()
        ordered_clients = ordered_clients.iloc[1:]
        ordered_clients["dist_from_origin"] = self.dist_matrix[0,1:]
        self.candidate_clients = ordered_clients.sort_values(by=["end_window", "dist_from_origin"], ascending = [True, False])
        self.feasible_clients = self.candidate_clients.copy()

        while self.candidate_clients.shape[0] > 0:
             if create_route:
                 inserted_client, create_route = self.create_route()
             else:
                 if self.feasible_clients.shape[0] == 0:
                     create_route = True
                 else:
                     self.filter_feasible_clients()
                     if self.feasible_clients.shape[0] == 0:
                         create_route = True
                     else:
                         insertion_position = self.get_insertion_position()

             self.routes.inventory.iloc[-1] += self.clients.query("id == @inserted_client").demand
             self.candidate_clients = self.candidate_clients.iloc[1:]
             self.feasible_clients = self.feasible_clients.iloc[1:]

    def get_dist_matrix(self):
        x_array = np.array([self.clients.x])
        y_array = np.array([self.clients.y])
        x_matrix = x_array.T - x_array
        y_matrix = y_array.T - y_array
        dist_matrix = x_matrix**2 + y_matrix**2
        dist_matrix = np.sqrt(dist_matrix)

        self.dist_matrix = dist_matrix

    def get_time_matrix(self):
        time_matrix = self.dist_matrix/self.velocity
        bool = np.array([[0] + list(np.ones(self.clients.shape[0]-1))]).T
        service_time = self.service_time*bool
        time_matrix += service_time

        self.time_matrix = time_matrix

    def create_route(self):

        client = self.candidate_clients.id.iloc[0]
        route = {
        "num_clients": 0,
        "instants": [0],
        "route_plan": [self.clients.id.iloc[0], client, self.clients.id.iloc[0]],
        "inventory": 0
        }
        self.routes = self.routes.append(route, ignore_index=True)
        self.routes.iloc[-1,:].instants += self.calc_inst(1, self.routes.shape[0])
        self.routes.iloc[-1,:].instants += self.calc_inst(len(self.routes.iloc[-1,:].instants)-1, self.routes.shape[0])

        return client, False

    def calc_inst(self, position, route_num):

        u = self.routes.iloc[route_num-1].route_plan[position-1]
        v = self.routes.iloc[route_num-1].route_plan[position]
        start_window_v = self.clients.query("id == @v").start_window.iloc[0]
        instant_u = self.routes.iloc[route_num-1].instants[position-1]

        if start_window_v > instant_u + self.time_matrix[u,v]:
            return start_window_v
        else:
            return instant_u + self.time_matrix[u,v]

    def filter_feasible_clients(self):

        inventory = self.routes.inventory.iloc[-1]
        for i in range(self.feasible_clients.shape[0]):
            client = self.feasible_clients.iloc[i]
            client_id = client.id
            demand = client.demand

            if inventory + demand > self.vehicle_capacity:
                index = self.feasible_clients.index[i]
                print(index)
                self.feasible_clients = self.feasible_clients.drop(index)
                if self.feasible_clients.shape[0] == 0:
                    break

    def get_insertion_position(self):

        pass

    def c1_cost(self, position, client_id):

        u = self.routes.route_plan.iloc[-1][position-1]
        v = client_id
        start_window_v = self.clients.query("id == @v").start_window
        end_window_v = self.clients.query("id == @v").end_window
        instant_u = self.routes.instants.iloc[-1][position-1]
        time = self.time_matrix[u,v]

        if start_window_v > instant_u + time:
            instant_v = start_window_v
        else:
            instant_v = instant_u + time

        if instant_v > end_window_v:
            return -1
        else:
            return 0

clients = pd.DataFrame([[1,15,1,2,3,4], [2,35,3,4,5,8], [3,50,5,6,1,7], [4,700,7,8,1,10], [5,210,9,10,1,10]], columns=["id", "demand", "x", "y", "start_window", "end_window"])

params = {"velocity": 10,
          "service_time": 0.1,
          "vehicle_capacity": 700}

heuristic = Heuristic(clients, params)
heuristic.get_dist_matrix()
heuristic.get_time_matrix()
ordered_clients = heuristic.clients.copy()
ordered_clients = ordered_clients.iloc[1:]
ordered_clients["dist_from_origin"] = heuristic.dist_matrix[0,1:]
heuristic.candidate_clients = ordered_clients.sort_values(by=["end_window", "dist_from_origin"], ascending = [True, False])
heuristic.feasible_clients = heuristic.candidate_clients.copy()

if __name__ == '__main__':
    inserted_client, create_route = heuristic.create_route()
    print(heuristic.candidate_clients)
    heuristic.routes.inventory.iloc[-1] += heuristic.clients.query("id == @inserted_client").demand.iloc[0]
    heuristic.candidate_clients = heuristic.candidate_clients.iloc[1:]
    heuristic.feasible_clients = heuristic.feasible_clients.iloc[1:]
    heuristic.filter_feasible_clients()
    print(heuristic.feasible_clients)
