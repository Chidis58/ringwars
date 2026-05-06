
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sim.scenarios.default import create_world
from sim.core.engine import Simulation
from sim.config import PARAMS
from sim.interactive.player import HumanPlayer

def main():
    print("=== RingWars Interactive Mode ===")
    
    ans = input("Do you want to participate? (y/n): ").strip().lower()
    if ans != 'y':
        print("Exiting.")
        return

    print("\nChoose role:")
    print("1 = Connector")
    print("2 = Node")
    role_choice = input("Choice: ").strip()
    
    role = 'connector' if role_choice == '1' else 'node'
    
    # Initialize world first to see what's available
    # We use a fixed seed for consistency if not specified
    seed = 42
    connectors, nodes = create_world(n_connectors=10, n_nodes=10, seed=seed)
    
    if role == 'connector':
        print("\nAvailable Connectors:")
        for cid in connectors.keys():
            print(f"  C{cid}")
        player_id = int(input("Select your ID: ").strip())
    else:
        print("\nAvailable Nodes:")
        for nid in nodes.keys():
            print(f"  N{nid}")
        player_id = int(input("Select your ID: ").strip())

    human = HumanPlayer(role, player_id)
    
    # Initialize simulation with human player
    sim = Simulation(connectors, nodes, PARAMS, verbose=True, seed=seed)
    sim.human_player = human
    
    days = 10
    print(f"\nStarting {days}-day simulation...")
    sim.run(days=days)

    print("\n--- FINAL RESULTS ---")
    if role == 'connector':
        me = sim.connectors[player_id]
        print(f"You (C{player_id}):")
        print(f"  Final Balance: {me.balance:.2f}")
        print(f"  Connections: {len(me.connections)}")
    else:
        me = sim.nodes[player_id]
        print(f"You (N{player_id}):")
        print(f"  Final Earnings: {me.earnings:.2f}")
        print(f"  Visit Load: {me.visit_load:.2f}")

    # Top winners
    top_c = sorted(sim.connectors.values(), key=lambda x: x.balance, reverse=True)[0]
    top_n = sorted(sim.nodes.values(), key=lambda x: x.earnings, reverse=True)[0]
    
    print(f"\nTop Connector: C{top_c.id} (Bal: {top_c.balance:.2f})")
    print(f"Top Node: N{top_n.id} (Earnings: {top_n.earnings:.2f})")

if __name__ == "__main__":
    main()
