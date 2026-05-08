
import random
import networkx as nx
import os
from .mechanics import compute_cost
from .logger import Logger
from ..observability.logger import ObservabilityLogger
from ..config import EXPERIMENTS

class Simulation:
    def __init__(self, connectors, nodes, params, verbose=True, seed=None, experiments=None):
        self.connectors = connectors
        self.nodes = nodes
        self.params = params
        self.experiments = experiments or EXPERIMENTS
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
        cost = compute_cost(c, node, overlap, self.params, self.experiments)

        # Log decision to observability layer
        self.obs_logger.log_decision(
            day, c.id, node.id, cost, c.personality if hasattr(c, 'personality') else {'human': 1}, reason
        )

        if c.balance < cost:
            self.obs_logger.log_event(day, "BANKRUPTCY_PREVENTED", {"connector_id": c.id, "node_id": node.id, "cost": cost})
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
            if node.visit_load >= self.params["visit_load_cap"]:
                self.obs_logger.log_event(day, "SATURATION_LOCK", {"node_id": node.id, "load": node.visit_load})
        else:
            node.visit_load = max(0, node.visit_load - 0.2)

        # Emoji logic (Keep UI/CLI frozen, but we use this for the human events log if needed)
        # Actually, let's just keep the existing events list for the UI print, 
        # and use obs_logger for raw events.

        # ring logic
        if cost > node.last_price:
            old_holder = node.ring_holder
            node.ring_holder = c.id
            node.last_price = cost
            node.streak += 1
            
            self.obs_logger.log_event(day, "RING_TRANSFER", {
                "node_id": node.id,
                "from_id": old_holder,
                "to_id": c.id,
                "cost": cost,
                "streak": node.streak
            })

            # EXPERIMENT: revenge_bidding
            if self.experiments.get("revenge_bidding") and old_holder is not None:
                if old_holder in self.connectors:
                    self.connectors[old_holder].revenge_targets.add(node.id)
                    self.obs_logger.log_event(day, "REVENGE_TRIGGERED", {"connector_id": old_holder, "node_id": node.id})

            old_fmt = self._fmt_c(old_holder) if old_holder is not None else "None"
            events.append(f"{self._fmt_c(c.id)} took 💍 of {self._fmt_n(node.id)} from {old_fmt} at 🪙{cost:.1f} ({reason})")
        else:
            type_label = "🔁REVISIT" if is_revisit else "🫂NEW"
            events.append(f"{self._fmt_c(c.id)} {type_label} {self._fmt_n(node.id)} at 🪙{cost:.1f} ({reason})")
            
            self.obs_logger.log_event(day, "CONNECTION_MADE", {
                "connector_id": c.id,
                "node_id": node.id,
                "is_revisit": is_revisit,
                "cost": cost
            })
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
                        "estimated_cost": compute_cost(me, n, overlap, self.params, self.experiments),
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
            node, reason = c.decide_node(self.nodes, self.experiments)
            if not node:
                continue
            self.process_connection(c, node, day, reason, events)

        # EXPERIMENT: ring_decay
        if self.experiments.get("ring_decay"):
            for n in self.nodes.values():
                if n.ring_holder is not None:
                    decay = n.last_price * 0.05 # 5% daily decay
                    n.last_price = max(10, n.last_price - decay)

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
            self.logger.log_day(day, events)
        
        snap = self.snapshot()
        self.history.append(snap)
        self.obs_logger.log_history(day, snap)

    def run(self, days=30, output_dir="sim/output"):
        for day in range(1, days + 1):
            self.day_step(day)
        
        if self.logger.verbose:
            self.logger.summary(self.connectors, self.nodes)

        # Export raw laboratory data
        metrics = self.snapshot()
        metrics["days"] = days
        metrics["experiment_flags"] = self.experiments
        self.obs_logger.export_data(output_dir, metrics)

        # Generate experiment_report.md
        report_path = os.path.join(output_dir, "experiment_report.md")
        with open(report_path, "w") as f:
            f.write(f"# EXPERIMENT: RingWars Lab Run\n\n")
            f.write("## INPUT\n")
            f.write("- Active Flags:\n")
            for flag, val in self.experiments.items():
                f.write(f"  - {flag}: {val}\n")
            f.write(f"- Days: {days}\n")
            f.write(f"- Seed: {self.seed}\n\n")
            
            f.write("## RESULTS\n")
            f.write(f"- Final Supply: {metrics['supply']:.2f} 🪙\n")
            f.write(f"- Platform Revenue: {metrics['revenue']:.2f} 🪙\n")
            f.write(f"- Total Burned: {metrics['burned']:.2f} 🪙\n")
            f.write(f"- Survival Rate: {metrics['survival_rate']*100:.1f}%\n")
            f.write(f"- Avg Visit Load: {metrics['avg_visit_load']:.2f}\n\n")
            
            f.write("## OBSERVATIONS\n")
            # Emergent behavior detection
            ring_transfers = sum(1 for e in self.obs_logger.events if e['type'] == 'RING_TRANSFER')
            bankruptcies = sum(1 for e in self.obs_logger.events if e['type'] == 'BANKRUPTCY_PREVENTED')
            f.write(f"- Ring Transfers: {ring_transfers}\n")
            f.write(f"- Bankruptcy Events (Prevented): {bankruptcies}\n")
            
            expensive = self.obs_logger.get_top_expensive(1)
            if expensive:
                f.write(f"- Peak Cost: 🪙{expensive[0]['cost']} at Node {expensive[0]['node_id']}\n")
            
            f.write("\n## CONCLUSION\n")
            f.write("- Mechanic impact: [To be analyzed based on metrics.json trends]\n")
            f.write("- Recommendation: [Keep / Modify / Discard based on emergent patterns]\n")

        print(f"\nLaboratory data and report exported to {output_dir}/")

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
