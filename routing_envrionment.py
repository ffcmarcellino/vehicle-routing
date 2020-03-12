class routingEnv():

    def __init__(self, params):
        self.t = 0
        # params

    def advance(self):

        self.update_inventories()
        self.sample_orders()
        self.create_routes()
        self.run_vehicles()
        self.place_orders()
        self.t += self.time_step

    def update_inventories(self):
        pass

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
