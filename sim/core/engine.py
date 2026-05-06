
import random
import networkx as nx
from .mechanics import compute_cost
from .logger import Logger

class Simulation:
    def __init__(self, connectors, nodes, params, verbose=True, seed=None):
        self.connectors = connectors
        self.nodes = nodes
        self.params = params
        self.logger = Logger(verbose=verbose)
        self.seed = seed
        self.rng = random.Random(seed)
        
        # Inject RNG into connectors
        for c in self.connectors.values():
            c.rng = self.rng

        self.platform_revenue = 0
        self.total_burned = 0
        self.total_spent = 0 

        self.history = []
        
        # 🔥 Social graph
        self.graph = nx.Graph()
        # Sort keys to ensure deterministic node addition
        for cid in sorted(connectors.keys()):
            self.graph.add_node(f"C{cid}", type="connector")

        for nid in sorted(nodes.keys()):
            self.graph.add_node(f"N{nid}", type="node")

    def cluster_overlap(self, connector_id, node_id):
        overlap = 0
        # networkx neighbors might not be sorted, but for a set/len it doesn't matter
        node_neighbors = set(self.graph.neighbors(f"N{node_id}"))

        for neighbor in node_neighbors:
            if neighbor.startswith("C") and neighbor != f"C{connector_id}":
                other_id = int(neighbor[1:])
                overlap += len(
                    self.connectors[connector_id].connections &
                    self.connectors[other_id].connections
                )
        return overlap

    def day_step(self, day):
        events = []
        # Daily activity: use self.rng
        all_cids = sorted(self.connectors.keys())
        active_connectors = [
            self.connectors[cid] for cid in all_cids 
            if self.connectors[cid].balance > 5 and self.rng.random() > 0.2
        ]
        
        self.rng.shuffle(active_connectors)

        for c in active_connectors:
            node = c.decide_node(self.nodes, {})
            if not node:
                continue

            overlap = self.cluster_overlap(c.id, node.id)
            cost = compute_cost(c, node, overlap, self.params)

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
            self.graph.add_edge(f"C{c.id}", f"N{node.id}")
            c.connections.add(node.id)
            node.connections.add(c.id)

            # visit load
            if overlap > 0:
                node.visit_load += 1
            else:
                node.visit_load = max(0, node.visit_load - 0.2)

            # ring logic
            if cost > node.last_price:
                old_holder = node.ring_holder
                node.ring_holder = c.id
                node.last_price = cost
                node.streak += 1
                events.append(f"C{c.id} took Ring of N{node.id} from C{old_holder} at {cost:.1f}")
            else:
                events.append(f"C{c.id} connected to N{node.id} at {cost:.1f}")

        self.logger.log_day(day, events)
        self.history.append(self.snapshot())

    def run(self, days=30):
        for day in range(1, days + 1):
            self.day_step(day)
        
        if self.logger.verbose:
            self.logger.summary(self.connectors, self.nodes)

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
