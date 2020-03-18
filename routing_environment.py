import datetime
import numpy as np

class routingEnv():

    def __init__(self, params):
        self.t = params.initial_time
        self.time_step = params.time_step
        self.origins = params.origins
        self.origin_types = params.origin_types
        self.product_types = params.product_types
        self.update_margin = params.update_margin
        self.probs = params.probs
        self.regions = params.regions
        self.clients = params.clients
        self.client_types = params.client_types
        self.orders = params.orders
        self.vehicle_types = params.vehicle_types
        self.vehicles = params.vehicles
        # self.clients region_id

    def advance(self):

        self.refill_inventories()
        self.sample_orders()
        self.create_routes()
        self.start_routes()
        self.run_vehicles()
        self.update_environment()
        self.t += datetime.timedelta(minutes = self.time_step)

    def refill_inventories(self):
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

    def start_routes(self):
        #update route status

        #update vehicle status
        #update vehicle destination
        #update vehicle inventory
        #update origin inventory
        pass

    def run_vehicles(self):

        delta_x = self.vehicles.x_dest - self.vehicles.x
        delta_y = self.vehicles.y_dest - self.vehicles.y
        hypothenuse = (delta_x**2 + delta_y**2)**(0.5)

        sin = delta_x/hypothenuse if hypothenuse != 0 else 0
        cos = delta_y/hypothenuse if hypothenuse != 0 else 0

        speed = self.vehicles.vehicle_type.apply(lambda x: self.vehicle_types[x]["speed"])
        x_speed = speed * sin
        y_speed = speed * cos

        self.vehicles.x = self.vehicles.x + x_speed * self.time_step
        self.vehicles.y = self.vehicles.y + y_speed * self.time_step

    def update_environment(self):

        has_arrived = self.vehicles.x == self.vehicles.x_dest and self.vehicles.y == self.vehicles.y_dest and self.vehicles.next_delivery != -1

        merged_vehicles = pd.merge(self.vehicles, self.routes, on = "route_id", how = "left")[["next_delivery", "route_plan"]]
        next_id = merged_vehicles.apply(lambda row: row.route_plan[row.next_delivery] if row.route_plan != 0 else 0)
        last_id = merged_vehicles.apply(lambda row: row.route_plan[-1] if row.route_plan != 0 else 0)

        is_origin = (next_id == last_id)

        for product in self.product_types.keys():
            qty = pd.merge(next_id, self.orders, on = "order_id", how = "left")[product]
            qty = qty.fillna(0)
            self.vehicles[product] -= qty * (1*(not is_origin and has_arrived))

        self.vehicles.next_delivery = self.vehicles.next_delivery * (1*(not has_arrived)) -1 * (1*(is_origin and has_arrived)) + (self.vehicles.next_delivery + 1) * (1*(not is_origin and has_arrived))
        self.vehicles.route_id = self.vehicles.route_id * (1*(not is_origin or (is_origin and not has_arrived)))

        order_ids = next_id[not is_origin and has_arrived]
        self.orders.status *= self.orders.apply(lambda row: 1*(row.order_id not in order_ids))

    def render_environment(self):
        pass
