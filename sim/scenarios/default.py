
import random
from ..agents.connector import Connector
from ..agents.node import Node

def create_world(n_connectors=20, n_nodes=20, seed=42):
    rng = random.Random(seed)
    
    strategies = ["AGGRESSIVE", "EXPLORER", "DEFENSIVE", "WHALE"]

    connectors = {}
    for i in range(n_connectors):
        strat = rng.choice(strategies)
        balance = rng.uniform(200, 500)
        if strat == "WHALE":
            balance *= 2 # Whales have more money
        
        connectors[i] = Connector(i, balance, {}, strategy=strat, rng=rng)

    nodes = {i: Node(i) for i in range(n_nodes)}
    return connectors, nodes
