from .entities import Connector, Node
from .engine import Simulation
from .config import PARAMS
from .visualize import plot_metrics, draw_graph
import random


def create_world(n_connectors=20, n_nodes=20):
    connectors = {
        i: Connector(i, random.uniform(200, 500), "balanced")
        for i in range(n_connectors)
    }

    nodes = {i: Node(i) for i in range(n_nodes)}
    return connectors, nodes



if __name__ == "__main__":
    connectors, nodes = create_world()

    sim = Simulation(connectors, nodes, PARAMS)
    sim.run(ticks=500)

    plot_metrics(sim.history)     # 📊 charts
    draw_graph(sim.graph)         # 🌐 network view

