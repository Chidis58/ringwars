
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
        self.human_history = []
        
        # 🔥 Social graph
        self.graph = nx.Graph()
        for cid in sorted(connectors.keys()):
            self.graph.add_node(f"C{cid}", type="connector")

        for nid in sorted(nodes.keys()):
            self.graph.add_node(f"N{nid}", type="node")

    def _fmt_c(self, cid):
        return f"🕺{cid}" if cid is not None else "None"

    def _fmt_n(self, nid):
        return f"💃{nid}" if nid is not None else "None"

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
        is_revisit = node.id in c.connections
        self.graph.add_edge(f"C{c.id}", f"N{node.id}")
        c.connections.add(node.id)
        node.connections.add(c.id)

        # visit load
        if overlap > 0:
            node.visit_load += 1
        else:
            node.visit_load = max(0, node.visit_load - 0.2)

        # Emoji logic
        symbol = "🔁" if is_revisit else "🤝"
        c_fmt = self._fmt_c(c.id)
        n_fmt = self._fmt_n(node.id)

        # ring logic
        if cost > node.last_price:
            old_holder = node.ring_holder
            node.ring_holder = c.id
            node.last_price = cost
            node.streak += 1
            old_fmt = self._fmt_c(old_holder) if old_holder is not None else "None"
            events.append(f"{c_fmt} took 💍 of {n_fmt} from {old_fmt} at 🪙{cost:.1f} ({reason})")
        else:
            type_label = "🔁REVISIT" if is_revisit else "🫂NEW"
            events.append(f"{c_fmt} {type_label} {n_fmt} at 🪙{cost:.1f} ({reason})")
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
                print(f"\n\n{'='*13} DAY {day}{'='*14}")
                print(f"🕺{me.id}, You have |🪙{me.balance:.2f} | 🫂{len(me.connections)}")
                
                # Pre-calculate node data
                nodes_state = {}
                me_connected = {}
                for nid, n in self.nodes.items():
                    overlap = self.cluster_overlap(me.id, n.id)
                    pressure = min(1.0, overlap / 5.0) 
                    is_revisit = nid in me.connections
                    me_connected[nid] = is_revisit
                    
                    recent = [
                        f"Day {d['day']}: {self._fmt_c(d['connector_id'])} {d['reason']} @ 🪙{d['cost']:.1f}"
                        for d in self.obs_logger.all_decisions 
                        if d['node_id'] == nid
                    ][-3:]

                    nodes_state[nid] = {
                        "estimated_cost": compute_cost(me, n, overlap, self.params),
                        "visit_load": n.visit_load,
                        "ring_holder": n.ring_holder if n.ring_holder is not None else "None",
                        "connected_connectors": sorted(list(n.connections)),
                        "recent_activity": recent,
                        "cluster_pressure": pressure
                    }

                state = {
                    "balance": me.balance,
                    "my_connections": len(me.connections),
                    "my_rings": sum(1 for n in self.nodes.values() if n.ring_holder == me.id),
                    "nodes": nodes_state,
                    "me_connected_to_target": me_connected
                }
                action = self.human_player.choose_action(state)
                if action['type'] == 'connect':
                    target_node = self.nodes[action['target']]
                    is_revisit = target_node.id in me.connections
                    verb = "🔁Revisited" if is_revisit else "🫂connected to"
                    success = self.process_connection(me, target_node, day, "human_choice", events)
                    if success:
                        human_action_log = f"you {verb} {self._fmt_n(target_node.id)}"
                    else:
                        human_action_log = f"attempted to 🫂connect to {self._fmt_n(target_node.id)} (Failed: Insufficient Balance)"
                elif action['type'] == 'exit':
                    print("Exiting simulation...")
                    self.logger.summary(self.connectors, self.nodes)
                    import sys
                    sys.exit(0)
                else:
                    human_action_log = "you skip"
                
                self.human_history.append(f"Day {day}: {human_action_log}")
            
            elif self.human_player.role == 'node':
                human_nid = self.human_player.id
                me = self.nodes[human_nid]
                print(f"\n\n{'='*13} DAY {day}{'='*14}")
                rh_fmt = self._fmt_c(me.ring_holder) if me.ring_holder is not None else "None"
                print(f"💃{me.id}, You have |🪙{me.earnings:.2f} | 🤱{me.visit_load:.2f} | 💍{rh_fmt}")
                state = {
                    "earnings": me.earnings,
                    "visit_load": me.visit_load,
                    "ring_holder": me.ring_holder
                }
                action = self.human_player.choose_action(state)
                if action['type'] == 'influence':
                    influence_map = {'encourage': 0.8, 'neutral': 1.0, 'discourage': 1.5}
                    me.influence = influence_map[action['mode']]
                    human_action_log = f"you set influence: {action['mode']}"
                else:
                    human_action_log = "you skip"
                
                self.human_history.append(f"Day {day}: {human_action_log}")

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
            for e in events[:5]:
                print(f"  {e}")
            
            snap = self.snapshot()
            print("\nSystem:")
            print(f"  Avg 🤱: {snap['avg_visit_load']:.2f}")
            print(f"  Total supply: 🪙{snap['supply']:.1f}")
            print("-" * 47)
        else:
            # For experiments/logger, also use emoji-friendly names if possible, 
            # but we'll stick to text-based logger to avoid breaking existing downstream parsers if any.
            # However, logger.py's log_day can be updated too.
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
