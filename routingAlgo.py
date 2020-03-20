class vehicleRouter():

    def __init__(self, vehicles):
        self.vehicles = vehicles
        self.routes = pd.DataFrame(columns=["route_id", "vehicle_type", "route_plan", "vehicle_id"])

    def route_moving_inventory(self):
        # roteirizar estoques moveis no meio da rota 
        pass

    def assign_origins():
        # associar clientes a origem
        pass

    def vrptw_heuristic():
        # vrptw
        pass

    def assign_final_dest():
        # calcular destinos finais
        pass
