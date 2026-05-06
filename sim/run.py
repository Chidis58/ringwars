
from sim.scenarios.default import create_world
from sim.core.engine import Simulation
from sim.config import PARAMS
import sys

def main():
    print("Initializing RingWars Simulation...")
    connectors, nodes = create_world(n_connectors=15, n_nodes=10)

    sim = Simulation(connectors, nodes, PARAMS)
    
    days = 10
    print(f"Running for {days} days...")
    sim.run(days=days)

if __name__ == "__main__":
    main()
