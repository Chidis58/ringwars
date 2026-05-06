
class Node:
    def __init__(self, id):
        self.id = id
        self.visit_load = 0
        self.connections = set()
        self.ring_holder = None
        self.last_price = 10
        self.earnings = 0
        self.streak = 0

    def __repr__(self):
        return f"<Node {self.id} | Load: {self.visit_load:.1f} | Ring: {self.ring_holder}>"
