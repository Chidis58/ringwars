import random

class Connector:
    def __init__(self, id, balance, personality, rng=None):
        self.id = id
        self.balance = balance
        self.personality = personality  # dict with weights: aggression, strategy, loyalty, chaos
        self.connections = set()
        self.conviction = {}  # node_id -> score
        self.active = True
        self.rng = rng or random.Random()

    def decide_node(self, nodes, context):
        """
        Decision logic based on personality.
        Returns: (Node, reason_string)
        """
        available_nodes = list(nodes.values())
        if not available_nodes:
            return None, "no_nodes"
        
        # Chaos weight
        if self.rng.random() < self.personality.get('chaos', 0.1):
            return self.rng.choice(available_nodes), "chaos"
        
        # Strategy: look for low visit load
        if self.personality.get('strategy', 0) > 0.5:
            available_nodes.sort(key=lambda n: (n.visit_load, n.id))
            return available_nodes[0], "strategy"

        # Aggression: look for high streak/contested nodes
        if self.personality.get('aggression', 0) > 0.5:
            available_nodes.sort(key=lambda n: (n.streak, n.id), reverse=True)
            return available_nodes[0], "aggression"

        return self.rng.choice(available_nodes), "random_fallback"

    def __repr__(self):
        return f"<Connector {self.id} | Bal: {self.balance:.1f} | Pers: {max(self.personality, key=self.personality.get)}>"
