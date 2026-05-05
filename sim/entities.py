
class Connector:
    def __init__(self, id, balance, strategy):
        self.id = id
        self.balance = balance
        self.connections = set()
        self.conviction = {}
        self.strategy = strategy


class Node:
    def __init__(self, id):
        self.id = id
        self.visit_load = 0
        self.connections = set()
        self.ring_holder = None
        self.last_price = 10
        self.earnings = 0
        self.streak = 0
