import random

class Connector:
    def __init__(self, id, balance, personality, strategy="EXPLORER", rng=None):
        self.id = id
        self.balance = balance
        self.personality = personality  # Keep for compatibility, but moving to strategy
        self.strategy = strategy # AGGRESSIVE, EXPLORER, DEFENSIVE, WHALE
        self.connections = set()
        self.conviction = {}  # node_id -> score
        self.revenge_targets = set() # node_ids where ring was recently stolen from us
        self.active = True
        self.rng = rng or random.Random()

    def decide_node(self, nodes, context):
        """
        Decision logic based on strategy.
        Returns: (Node, reason_string)
        """
        available_nodes = list(nodes.values())
        if not available_nodes:
            return None, "no_nodes"

        # EXPERIMENT: revenge_bidding
        if context.get("revenge_bidding") and self.revenge_targets:
            # Pick a revenge target if we can afford it (simple check)
            for rid in list(self.revenge_targets):
                if rid in nodes:
                    node = nodes[rid]
                    if node.ring_holder != self.id:
                        # Clean up if we already got it back or if we choose to pursue it
                        self.revenge_targets.remove(rid)
                        return node, "revenge"

        # AGGRESSIVE: Targets highly contested nodes (high streak) and spends regardless of load.
        if self.strategy == "AGGRESSIVE":
            available_nodes.sort(key=lambda n: (n.streak, n.id), reverse=True)
            return available_nodes[0], "aggression"
        
        # EXPLORER: Targets low visit load nodes to find cheap connections.
        elif self.strategy == "EXPLORER":
            available_nodes.sort(key=lambda n: (n.visit_load, n.id))
            return available_nodes[0], "exploration"
        
        # DEFENSIVE: Targets nodes it already owns (revisits) to protect them.
        elif self.strategy == "DEFENSIVE":
            my_owned = [n for n in available_nodes if n.ring_holder == self.id]
            if my_owned:
                my_owned.sort(key=lambda n: (n.visit_load, n.id), reverse=True)
                return my_owned[0], "defense"
            # Fallback to explorer if nothing owned
            available_nodes.sort(key=lambda n: (n.visit_load, n.id))
            return available_nodes[0], "fallback_exploration"
        
        # WHALE: High balance players that target nodes with highest price to dominate.
        elif self.strategy == "WHALE":
            available_nodes.sort(key=lambda n: (n.last_price, n.id), reverse=True)
            return available_nodes[0], "dominance"

        # Legacy personality logic
        if self.rng.random() < self.personality.get('chaos', 0.1):
            return self.rng.choice(available_nodes), "chaos"
        
        if self.personality.get('strategy', 0) > 0.5:
            available_nodes.sort(key=lambda n: (n.visit_load, n.id))
            return available_nodes[0], "strategy"

        return self.rng.choice(available_nodes), "random_fallback"

    def __repr__(self):
        return f"<Connector {self.id} | Bal: {self.balance:.1f} | Strat: {self.strategy}>"
