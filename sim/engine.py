
import random
from .mechanics import compute_cost, cluster_overlap
from .metrics import summarize
import networkx as nx

class Simulation:
    def __init__(self, connectors, nodes, params):
        self.connectors = connectors
        self.nodes = nodes
        self.params = params

        self.platform_revenue = 0
        self.total_burned = 0
        self.total_spent = 0 

        self.history = []
        
        # 🔥 Social graph
        self.graph = nx.Graph()
        for c in connectors:
            self.graph.add_node(f"C{c}", type="connector")

        for n in nodes:
            self.graph.add_node(f"N{n}", type="node")
    def cluster_overlap(self, connector_id, node_id):
        overlap = 0
        node_neighbors = set(self.graph.neighbors(f"N{node_id}"))

        for neighbor in node_neighbors:
            if neighbor.startswith("C") and neighbor != f"C{connector_id}":
                other_id = int(neighbor[1:])
                overlap += len(
                    self.connectors[connector_id].connections &
                    self.connectors[other_id].connections
                )
        return overlap
    
    def step(self):
        for cid, c in self.connectors.items():

            if c.balance < 5:
                continue

            node_id = random.choice(list(self.nodes.keys()))
            node = self.nodes[node_id]

            overlap = self.cluster_overlap(cid, node_id)

            cost = self.params["base_cost"] * (
                1 + overlap * self.params["overlap_factor"]
            ) * (1 + node.visit_load / self.params["visit_load_cap"])

            if c.balance < cost:
                continue

            # spend
            c.balance -= cost
            self.total_spent += cost

            burn = cost * self.params["burn_rate"]
            platform = cost * self.params["platform_cut"]
            node_share = cost * self.params["node_share"]

            self.total_burned += burn
            self.platform_revenue += platform
            node.earnings += node_share

            # graph update
            self.graph.add_edge(f"C{cid}", f"N{node_id}")

            # connections
            c.connections.add(node_id)
            node.connections.add(cid)

            # visit load
            if overlap > 0:
                node.visit_load += 1
            else:
                node.visit_load = max(0, node.visit_load - 0.2)

            # ring logic
            if cost > node.last_price:
                node.ring_holder = cid
                node.last_price = cost
                node.streak += 1


    def run(self, ticks=500, reset_history=True):
        if reset_history:
            self.history = []

        for _ in range(ticks):
            self.step()
            self.history.append(self.snapshot())

    def snapshot(self):
        total_supply = sum(c.balance for c in self.connectors.values())
        avg_visit_load = sum(n.visit_load for n in self.nodes.values()) / len(self.nodes)
        survival = sum(1 for c in self.connectors.values() if c.balance > 0)

        return {
            "supply": total_supply,
            "burned": self.total_burned,
            "revenue": self.platform_revenue,
            "avg_visit_load": avg_visit_load,
            "survival_rate": survival / len(self.connectors),
        }


