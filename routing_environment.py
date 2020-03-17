import datetime
import numpy as np

class routingEnv():

    def __init__(self, params):
        self.t = params.initial_time
        self.origins = params.origins
        self.origin_types = params.origin_types
        self.product_types = params.product_types
        self.update_margin = params.update_margin
        self.probs = params.probs
        self.regions = params.regions
        self.clients = params.clients
        self.client_types = params.client_types
        self.orders = params.orders
        # self.clients region_id

    def advance(self):

        self.update_inventories()
        self.sample_orders()
        self.create_routes()
        self.run_vehicles()
        self.place_orders()
        self.t += datetime.timedelta(minutes = self.time_step)

    def update_inventories(self):
        # origins = [id, type, x, y, p1, p2, p3, ..., pn]
        for product in self.product_types.keys():
            capacity = self.origin_types[origin["type"]]["capacity"][product]
            below = 1*(self.origins[product] <= self.update_margin * capacity)
            above = 1*(self.origins[product] > self.update_margin * capacity)
            self.origins[product] = self.origins[product] * above + below * capacity

    def sample_orders(self):
        num_products = len(product_types.keys())

        rand_order = np.random.random()
        if rand_order >= self.probs["order"]:
            return 0

        order = dict()
        order["order_id"] = self.orders.shape[0] + 1

        region_id = np.random.choice(self.regions.keys(), self.probs["region"])
        region = self.regions[region_id]

        products = np.array(self.product_types.keys())
        product_filter = np.less(np.random.random(num_products), self.probs["products"][region_id])
        products = products[product_filter]

        client_ids = self.clients.filter("region_id == @region_id").client_ids
        client_id = np.random.choice(client_ids)
        order["client_id"] = client_id

        time_window = np.random.randint(low=1, high=23)
        time_delta = np.random.randint(low=1 + time_window, high= 24)
        order["window_end"] = self.t + datetime.timedelta(hours = time_delta)
        order["window_start"] = self.t + datetime.timedelta(hours = time_delta - time_window)

        for product in products:
            std_qty = self.client_types[self.clients.filter("client_id == @client_id")["client_type"]]["std_qty"][product]
            perc =  time_delta * (1-self.probs["min_qty_perc"]) / 23 + 24 * self.probs["min_qty_perc"] / 23
            order[product] = (np.random.normal()*self.probs["std_dev_perc"] + 1) * std_qty * perc

        order["status"] = 1

        self.orders = self.orders.append(order, ignore_index=True)

    def create_routes(self):
        pass

    def run_vehicles(self):
        pass

    def place_orders(self):
        pass

    def render_environment(self):
        pass
