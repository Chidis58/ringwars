
import random
from ..agents.connector import Connector
from ..agents.node import Node

def create_world(n_connectors=20, n_nodes=20, seed=42):
    rng = random.Random(seed)
    
    personalities = [
        {"aggression": 0.8, "strategy": 0.1, "loyalty": 0.1},
        {"aggression": 0.1, "strategy": 0.8, "loyalty": 0.1},
        {"aggression": 0.1, "strategy": 0.1, "loyalty": 0.8},
        {"chaos": 0.9}
    ]

    connectors = {}
    for i in range(n_connectors):
        pers = rng.choice(personalities)
        connectors[i] = Connector(i, rng.uniform(200, 500), pers, rng=rng)

    nodes = {i: Node(i) for i in range(n_nodes)}
    return connectors, nodes
