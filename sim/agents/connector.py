import random

class Connector:
    def __init__(self, id, balance, personality):
        self.id = id
        self.balance = balance
        self.personality = personality  # dict with weights: aggression, strategy, loyalty, chaos
        self.connections = set()
        self.conviction = {}  # node_id -> score
        self.active = True

    def decide_node(self, nodes, context):
        """
        Decision logic based on personality.
        context: might include current market prices, graph state, etc.
        """
        # Simple implementation for now
        available_nodes = list(nodes.values())
        if not available_nodes:
            return None
        
        # Chaos weight
        if random.random() < self.personality.get('chaos', 0.1):
            return random.choice(available_nodes)
        
        # Strategy: look for low visit load
        if self.personality.get('strategy', 0) > 0.5:
            available_nodes.sort(key=lambda n: n.visit_load)
            return available_nodes[0]

        # Aggression: look for high streak/contested nodes
        if self.personality.get('aggression', 0) > 0.5:
            available_nodes.sort(key=lambda n: n.streak, reverse=True)
            return available_nodes[0]

        return random.choice(available_nodes)

    def __repr__(self):
        return f"<Connector {self.id} | Bal: {self.balance:.1f} | Pers: {max(self.personality, key=self.personality.get)}>"
