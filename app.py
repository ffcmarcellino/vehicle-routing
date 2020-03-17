import routing_environment
import datetime

env = routingEnv(params)
# params = ...
# datetime.datetime(2020, 3, 11, 15, 30)
duration = 180 # minutes

while env.t < env.t + datetime.timedelta(minutes = duration):
    env.advance()
    env.render_environment()
