import numpy as np
import pandas as pd

class Heuristic():

    def __init__(self, clients, params):
        self.clients = clients
        self.num_clients = self.clients.shape[0]-2
        self.velocity = params["velocity"]
        self.service_time = params["service_time"]
        self.routes = pd.DataFrame(columns=["num_clients", "instants", "route_plan", "inventory"])

    def heurisitc_algo(self):
        create_route = True
        self.get_dist_matrix()
        self.get_time_matrix()
        ordered_clients = self.clients[["id", "end_window"]]
        ordered_clients["dist_from_origin"] = self.dist_matrix[0,1:self.num_clients+1]
        ordered_clients = ordered_clients.sort_values(by=["end_window", "dist_from_origin"])

        # for i in range():
        #     if create_route:
        #         create_route = self.create_route(ordered_clients)
        #     else:
        #         'Filtra os clientes infactíveis em relação à restrição de capacidade. Se não houver cliente factível, uma nova rota será iniciada
        #     If num_capfeas = 0 Then
        #         create_route = 1
        #         GoTo Final_loop_line
        #     Else
        #         ReDim Preserve cap_feasible(1 To num_capfeas) As Integer
        #         i = 1
        #         Do While i <= num_capfeas
        #             aux = cap_feasible(i)
        #             If cap_util(n_vehic) + demand(aux) > capacity Then
        #                 i = i - 1
        #                 Call remove_client(cap_feasible, aux, num_capfeas)
        #                 num_capfeas = num_capfeas - 1
        #                 If num_capfeas = 0 Then
        #                     create_route = 1
        #                     Exit Do
        #                 End If
        #                 ReDim Preserve cap_feasible(1 To num_capfeas) As Integer
        #             End If
        #             i = i + 1
        #         Loop
        #     End If
        #     If create_route = 1 Then
        #         GoTo Final_loop_line
        #     End If
        #
        #     'Para cada cliente factível, calcula o termo c1 da heurística I1 de Solomon (1987) e a respectiva posição de inserção
        #     For i = 1 To num_capfeas
        #         new_min = c1(cost_matrix, rcost_matrix, time_matrix, position, 1, instant, start_window, end_window, n_vehic, num_clients(n_vehic), cap_feasible(i), mi, alpha1, alpha2, vr_machine(cap_feasible(i)), return_route(n_vehic))
        #         p_min = 1
        #         For j = 2 To num_clients(n_vehic) + 1
        #             aux_min = c1(cost_matrix, rcost_matrix, time_matrix, position, j, instant, start_window, end_window, n_vehic, num_clients(n_vehic), cap_feasible(i), mi, alpha1, alpha2, vr_machine(cap_feasible(i)), return_route(n_vehic))
        #             If new_min = "NA" Or (aux_min <> "NA" And aux_min <= new_min) Then
        #                 new_min = aux_min
        #                 p_min = j
        #             End If
        #         Next j
        #         ReDim Preserve c1_matrix(1 To i) As MyType
        #         c1_matrix(i).client = cap_feasible(i)
        #         c1_matrix(i).position = p_min
        #         c1_matrix(i).c1 = new_min
        #
        #     Next i
        #
        #     'Se não houver cliente factível quanto à restrição de janelas de tempo, cria uma nova rota
        #     For i = 1 To num_capfeas
        #         If c1_matrix(i).c1 <> "NA" Then
        #             Exit For
        #         End If
        #     Next i
        #     If i = num_capfeas + 1 Then
        #         create_route = 1
        #         GoTo Final_loop_line
        #     'Senão, identifica o cliente u a ser inserido na rota
        #     Else
        #         'Calcula o termo c2 da heurística I1 de Solomon(1987) para cada cliente factível
        #         j = 0
        #         For i = 1 To num_capfeas
        #             If c1_matrix(i).c1 <> "NA" Then
        #                 j = j + 1
        #                 ReDim Preserve c1c2_matrix(1 To j) As MyType
        #                 c1c2_matrix(j).client = c1_matrix(i).client
        #                 c1c2_matrix(j).position = c1_matrix(i).position
        #                 c1c2_matrix(j).c1 = c1_matrix(i).c1
        #                 c1c2_matrix(j).c2 = cost_matrix(0, cap_feasible(i)) - c1_matrix(i).c1
        #             End If
        #         Next i
        #         num_feas = j
        #         'Identifica o cliente u com o valor máx de c2
        #         new_max = c1c2_matrix(1).c2
        #         p_max = c1c2_matrix(1).position
        #         u = c1c2_matrix(1).client
        #
        #         If num_feas > 1 Then
        #             For i = 2 To num_feas
        #                 If c1c2_matrix(i).c2 >= new_max Then
        #                     new_max = c1c2_matrix(i).c2
        #                     p_max = c1c2_matrix(i).position
        #                     u = c1c2_matrix(i).client
        #                 End If
        #             Next i
        #         End If
        #         'Atualiza as posições da rota
        #         For i = num_clients(n_vehic) + 1 To p_max Step -1
        #             position(i + 1, n_vehic) = position(i, n_vehic)
        #         Next i
        #         position(p_max, n_vehic) = u
        #         'Atualiza os instantes
        #         For i = p_max To num_clients(n_vehic) + 2
        #             instant(position(i, n_vehic), n_vehic) = calc_inst(start_window, instant, time_matrix, position, i, n_vehic)
        #         Next i
        #     End If

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
        bool = np.array([[0] + list(np.ones(self.num_clients)) + [0]]).T
        service_time = self.service_time*bool
        time_matrix += service_time

        self.time_matrix = time_matrix

    def create_route(self, ordered_clients):

        self.feasible_clients = ordered_clients.id
        client = self.feasible_clients.iloc[0]
        route = {
        "num_clients": 0,
        "instants": [0],
        "route_plan": [self.clients.id.iloc[0], client, self.clients.id.iloc[0]],
        "inventory": 0
        }
        self.routes = self.routes.append(route, ignore_index=True)
        self.routes.iloc[-1,:].instants += self.calc_inst(1, self.routes.shape[0])
        self.routes.iloc[-1,:].instants += self.calc_inst(len(self.routes.iloc[-1,:].instants)-1, self.routes.shape[0])

        return False

    def calc_inst(self, position, route_num):

        u = self.routes.iloc[route_num-1].route_plan[position-1]
        v = self.routes.iloc[route_num-1].route_plan[position]
        start_window_v = self.clients.query("id == @v").start_window.iloc[0]
        instant_u = self.routes.iloc[route_num-1].instants[position-1]

        if start_window_v > instant_u + self.time_matrix[u,v]:
            return start_window_v
        else:
            return instant_u + self.time_matrix[u,v]

clients = pd.DataFrame([[1,10,1,2,3,4], [2,15,3,4,5,8], [3,21,5,6,1,7]], columns=["id", "demand", "x", "y", "start_window", "end_window"])
params = {"velocity": 10,
          "service_time": 1/12}
heuristic = Heuristic(clients, params)
heuristic.get_dist_matrix()
heuristic.get_time_matrix()
ordered_clients = heuristic.clients[["id", "end_window"]]
ordered_clients["dist_from_origin"] = heuristic.dist_matrix[0,:]
ordered_clients = ordered_clients.iloc[1:heuristic.num_clients+1,:]
ordered_clients = ordered_clients.sort_values(by=["end_window", "dist_from_origin"])

if __name__ == '__main__':
    print(heuristic.create_route(ordered_clients))
    print(heuristic.routes)
