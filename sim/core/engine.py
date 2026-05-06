
import random
import networkx as nx
from .mechanics import compute_cost
from .logger import Logger
from ..observability.logger import ObservabilityLogger

class Simulation:
    def __init__(self, connectors, nodes, params, verbose=True, seed=None):
        self.connectors = connectors
        self.nodes = nodes
        self.params = params
        self.logger = Logger(verbose=verbose)
        self.obs_logger = ObservabilityLogger()
        self.seed = seed
        self.rng = random.Random(seed)
        self.human_player = None
        
        # Inject RNG into connectors
        for c in self.connectors.values():
            c.rng = self.rng

        self.platform_revenue = 0
        self.total_burned = 0
        self.total_spent = 0 

        self.history = []
        
        # 🔥 Social graph
        self.graph = nx.Graph()
        for cid in sorted(connectors.keys()):
            self.graph.add_node(f"C{cid}", type="connector")

        for nid in sorted(nodes.keys()):
            self.graph.add_node(f"N{nid}", type="node")

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

    def process_connection(self, c, node, day, reason, events):
        overlap = self.cluster_overlap(c.id, node.id)
        cost = compute_cost(c, node, overlap, self.params)

        # Log decision to observability layer
        self.obs_logger.log_decision(
            day, c.id, node.id, cost, c.personality if hasattr(c, 'personality') else {'human': 1}, reason
        )

        if c.balance < cost:
            return False

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
            events.append(f"C{c.id} took Ring of N{node.id} from C{old_holder} at {cost:.1f} ({reason})")
        else:
            events.append(f"C{c.id} connected to N{node.id} at {cost:.1f} ({reason})")
        return True

    def day_step(self, day):
        events = []
        human_cid = None
        human_action_log = "None"
        
        # 1. Handle Human Player
        if self.human_player:
            if self.human_player.role == 'connector':
                human_cid = self.human_player.id
                me = self.connectors[human_cid]
                print(f"\n--- DAY {day} ---")
                print(f"STATUS: Balance: {me.balance:.2f} | Connections: {len(me.connections)}")
                state = {
                    "balance": me.balance,
                    "nodes": {
                        nid: {
                            "estimated_cost": compute_cost(me, n, self.cluster_overlap(me.id, n.id), self.params),
                            "visit_load": n.visit_load,
                            "ring_holder": n.ring_holder
                        } for nid, n in self.nodes.items()
                    }
                }
                action = self.human_player.choose_action(state)
                if action['type'] == 'connect':
                    target_node = self.nodes[action['target']]
                    success = self.process_connection(me, target_node, day, "human_choice", events)
                    if success:
                        human_action_log = f"C{me.id} → N{target_node.id}"
                else:
                    human_action_log = "Skip"
            
            elif self.human_player.role == 'node':
                human_nid = self.human_player.id
                me = self.nodes[human_nid]
                print(f"\n--- DAY {day} ---")
                print(f"STATUS: Earnings: {me.earnings:.2f} | Visit Load: {me.visit_load:.2f} | Ring Holder: {me.ring_holder}")
                state = {
                    "earnings": me.earnings,
                    "visit_load": me.visit_load,
                    "ring_holder": me.ring_holder
                }
                action = self.human_player.choose_action(state)
                if action['type'] == 'influence':
                    influence_map = {'encourage': 0.8, 'neutral': 1.0, 'discourage': 1.5}
                    me.influence = influence_map[action['mode']]
                    human_action_log = f"Set influence: {action['mode']}"
                else:
                    human_action_log = "Skip"

        # 2. Handle AI Agents
        all_cids = sorted(self.connectors.keys())
        active_connectors = [
            self.connectors[cid] for cid in all_cids 
            if cid != human_cid and self.connectors[cid].balance > 5 and self.rng.random() > 0.2
        ]
        
        self.rng.shuffle(active_connectors)

        for c in active_connectors:
            node, reason = c.decide_node(self.nodes, {})
            if not node:
                continue
            self.process_connection(c, node, day, reason, events)

        if self.human_player:
            print(f"Your action: {human_action_log}")
            print("Top events:")
            # Show top 5 events
            for e in events[:5]:
                print(f"  {e}")
            
            snap = self.snapshot()
            print("\nSystem:")
            print(f"  Avg ⤵️: {snap['avg_visit_load']:.2f}")
            print(f"  Total supply: {snap['supply']:.1f}")
            print("-" * 20)
        else:
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
