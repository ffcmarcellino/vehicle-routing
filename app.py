import routingEnvironment
import datetime

env = routingEnv(params)
# params = ...
# datetime.datetime(2020, 3, 11, 15, 30)
duration = 180 # minutes

while env.t < env.t + datetime.timedelta(minutes = duration):
    env.advance()
    env.render_environment()

# Objetos: veículos, origens, pedidos, clientes


# inicializar estado (posicao veiculos, destino, estoques, demandas)

#for t < T:

# recarregar estoques

# sample pedido

# roteirizar
    # roteirizar estoques moveis no meio da rota
    # associar clientes a origem
    # vrptw
    # calcular destinos finais
    # atualizar rotas
    # atualizar destinos veículos

# avançar veículos

# entregar pedidos
    ## atualizar status veiculo
    ## atualizar status pedido

# renderizar
