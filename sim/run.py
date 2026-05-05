import random
from .entities import Connector, Node
from .engine import Simulation
from .config import PARAMS
from .metrics import summarize

def create_world(n_connectors=50, n_nodes=20):
    connectors = {
        i: Connector(i, random.uniform(200, 500), random.choice(["explore", "compete", "balanced"]))
        for i in range(n_connectors)
    }

    nodes = {i: Node(i) for i in range(n_nodes)}
    return connectors, nodes


if __name__ == "__main__":
    connectors, nodes = create_world()
    sim = Simulation(connectors, nodes, PARAMS)

    sim.run(ticks=500)

    print(summarize(sim))
