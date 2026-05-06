
import random
from ..agents.connector import Connector
from ..agents.node import Node

def create_world(n_connectors=20, n_nodes=20):
    personalities = [
        {"aggression": 0.8, "strategy": 0.1, "loyalty": 0.1},
        {"aggression": 0.1, "strategy": 0.8, "loyalty": 0.1},
        {"aggression": 0.1, "strategy": 0.1, "loyalty": 0.8},
        {"chaos": 0.9}
    ]

    connectors = {}
    for i in range(n_connectors):
        pers = random.choice(personalities)
        connectors[i] = Connector(i, random.uniform(200, 500), pers)

    nodes = {i: Node(i) for i in range(n_nodes)}
    return connectors, nodes
