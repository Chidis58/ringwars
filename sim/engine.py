
import random
from .mechanics import compute_cost, cluster_overlap

class Simulation:
    def __init__(self, connectors, nodes, params):
        self.connectors = connectors
        self.nodes = nodes
        self.params = params
        self.platform_revenue = 0
        self.total_burned = 0

    def step(self):
        for c in self.connectors.values():
            if c.balance < 5:
                continue

            node = random.choice(list(self.nodes.values()))
            overlap = cluster_overlap(c, node, self.connectors)
            cost = compute_cost(c, node, overlap, self.params)

            if c.balance < cost:
                continue

            c.balance -= cost

            burn = cost * self.params["burn_rate"]
            platform = cost * self.params["platform_cut"]
            node_share = cost * self.params["node_share"]

            self.total_burned += burn
            self.platform_revenue += platform
            node.earnings += node_share

            c.connections.add(node.id)
            node.connections.add(c.id)

            if overlap > 0:
                node.visit_load += 1
            else:
                node.visit_load = max(0, node.visit_load - 0.2)

            if cost > node.last_price:
                node.ring_holder = c.id
                node.last_price = cost
                node.streak += 1

    def run(self, ticks=100):
        for _ in range(ticks):
            self.step()
