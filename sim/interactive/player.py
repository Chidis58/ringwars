
class HumanPlayer:
    def __init__(self, role, player_id):
        self.role = role # 'connector' or 'node'
        self.id = player_id

    def choose_action(self, state):
        """
        state: dict containing relevant simulation data
        """
        print(f"\n--- YOUR TURN ({self.role.upper()} {'C' if self.role == 'connector' else 'N'}{self.id}) ---")
        
        if self.role == 'connector':
            return self._connector_turn(state)
        else:
            return self._node_turn(state)

    def _connector_turn(self, state):
        balance = state['balance']
        nodes = state['nodes']
        print(f"Your Balance: {balance:.2f}")
        print("Available Nodes:")
        for nid, n_info in nodes.items():
            print(f"  N{nid}: Cost ~{n_info['estimated_cost']:.1f} | Load: {n_info['visit_load']:.1f} | Ring: {n_info['ring_holder']}")
        
        while True:
            choice = input("\nEnter Node ID to connect or 'skip': ").strip().lower()
            if choice == 'skip':
                return {"type": "skip"}
            try:
                node_id = int(choice)
                if node_id in nodes:
                    return {"type": "connect", "target": node_id}
                else:
                    print("Invalid Node ID.")
            except ValueError:
                print("Please enter a number or 'skip'.")

    def _node_turn(self, state):
        earnings = state['earnings']
        load = state['visit_load']
        ring = state['ring_holder']
        print(f"Your Earnings: {earnings:.2f} | Visit Load: {load:.2f} | Ring Holder: {ring}")
        
        print("\nActions:")
        print("  1 = Encourage (Reduce cost for others)")
        print("  2 = Neutral")
        print("  3 = Discourage (Increase cost for others)")
        
        while True:
            choice = input("\nChoose action (1-3) or 'skip': ").strip().lower()
            if choice == 'skip':
                return {"type": "skip"}
            if choice in ['1', '2', '3']:
                mode_map = {'1': 'encourage', '2': 'neutral', '3': 'discourage'}
                return {"type": "influence", "mode": mode_map[choice]}
            else:
                print("Invalid choice.")
