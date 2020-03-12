import multiprocessing as mp

pool = mp.Pool(mp.cpu_count())

class routingEnv():

    def __init__(self, params):
        self.t = 0
        self.origins = params.origins
        self.origin_types = params.origin_types
        self.product_types = params.product_types
        self.update_margin = params.update_margin
        # params

    def advance(self):

        self.update_inventories()
        self.sample_orders()
        self.create_routes()
        self.run_vehicles()
        self.place_orders()
        self.t += self.time_step

    def update_inventories(self):
        # origins = [id, type, x, y, p1, p2, p3, ..., pn]
        for product in self.product_types.keys():
            capacity = self.origin_types[origin["type"]]["capacity"][product]
            below = 1*(self.origins[product] <= self.update_margin * capacity)
            above = 1*(self.origins[product] > self.update_margin * capacity)
            self.origins[product] = self.origins[product] * above + below * capacity

    def sample_orders(self):
        pass

    def create_routes(self):
        pass

    def run_vehicles(self):
        pass

    def place_orders(self):
        pass

    def render_environment(self):
        pass
