
class HumanPlayer:
    def __init__(self, role, player_id):
        self.role = role # 'connector' or 'node'
        self.id = player_id

    def _fmt_c(self, cid):
        return f"🕺{cid}" if cid is not None else "None"

    def _fmt_n(self, nid):
        return f"💃{nid}" if nid is not None else "None"

    def choose_action(self, state):
        """
        state: dict containing relevant simulation data
        """
        if self.role == 'connector':
            return self._connector_turn(state)
        else:
            return self._node_turn(state)

    def _connector_turn(self, state):
        balance = state['balance']
        nodes = state['nodes']
        
        while True:
            print(f"👉[connect<id>, view:v<id>, Stat:s, Next:>, End:<<]")
            cmd_input = input(">>>:").strip().lower()
            
            if not cmd_input:
                continue

            if cmd_input == 's':
                # My stats
                print("\n--- My Stats ---")
                print(f"Role: {self._fmt_c(self.id)}")
                print(f"Balance: 🪙{balance:.2f}")
                print(f"🫂 Count: {state['my_connections']}")
                print(f"Owned Rings Count: {state['my_rings']}")
                
                # Network Map
                print("\n--- Network Map ---")
                for nid in sorted(nodes.keys()):
                    n_info = nodes[nid]
                    rh = n_info['ring_holder']
                    rh_fmt = self._fmt_c(rh) if isinstance(rh, int) else rh
                    hot = " 🔥" if n_info['visit_load'] > 5.0 or len(n_info['recent_activity']) > 2 else ""
                    print(f"  {self._fmt_n(nid):4} | 🤱 {n_info['visit_load']:.1f} | 💍 {rh_fmt}{hot}")
                continue

            elif cmd_input == '>':
                return {"type": "skip"}
            
            elif cmd_input == '<<':
                return {"type": "exit"}

            elif cmd_input.startswith('v'):
                raw_id = cmd_input[1:].strip()
                target_id = self._parse_id(raw_id)
                if target_id is not None and target_id in nodes:
                    self._show_node_detail(target_id, nodes[target_id])
                else:
                    print(f"Error: Invalid or missing Node ID for view.")
                continue

            else:
                # Try raw ID for quick connection
                target_id = self._parse_id(cmd_input)
                if target_id is not None and target_id in nodes:
                    # Proceed immediately as requested
                    return {"type": "connect", "target": target_id}
                print(f"Unknown command: {cmd_input}. Type ID to connect, 'v[id]' to view, 's' for stats, '>' to skip, or '<<' to exit.")

    def _confirm_action(self, action, state):
        # Removed as per instruction: "Remove: 'Proceed? (y/n):'"
        return True

    def _parse_id(self, val):
        clean = val.replace('n', '').replace('c', '').replace('💃', '').replace('🕺', '')
        try:
            return int(clean)
        except ValueError:
            return None

    def _show_node_detail(self, node_id, n_info):
        rh = n_info['ring_holder']
        rh_fmt = self._fmt_c(rh) if isinstance(rh, int) else rh
        print(f"\n--- Node {self._fmt_n(node_id)} Detail ---")
        print(f"Ring Holder: {rh_fmt}")
        print(f"Visit Load: 🤱 {n_info['visit_load']:.2f}")
        print(f"Estimated Cost: 🪙{n_info['estimated_cost']:.2f}")
        print(f"Active Connectors: {', '.join([self._fmt_c(c) for c in n_info['connected_connectors']]) if n_info['connected_connectors'] else 'None'}")
        
        print("\nRecent Activity:")
        if not n_info['recent_activity']:
            print("  (No recent activity)")
        else:
            for act in n_info['recent_activity']:
                print(f"  - {act}")
            
        pressure = n_info['cluster_pressure']
        pressure_label = "Low" if pressure < 0.3 else "Medium" if pressure < 0.7 else "High"
        print(f"\nCluster Pressure: {pressure_label} ({pressure:.2f})")
        
        # Insight
        if n_info['ring_holder'] == 'None':
            print("Insight: This node is currently unclaimed. Low cost opportunity.")
        elif pressure > 0.8:
            print("Insight: Extremely high congestion. Entry will be very expensive.")
        elif pressure < 0.2:
            print("Insight: Quiet zone. Good for stealth conviction building.")
        else:
            print("Insight: Active competition. Watch your balance.")

    def _node_turn(self, state):
        earnings = state['earnings']
        load = state['visit_load']
        ring = state['ring_holder']
        ring_fmt = self._fmt_c(ring) if isinstance(ring, int) else ring
        print(f"👉[influence:1-3, Next:>, End:<<]")
        
        while True:
            choice = input(">>>:").strip().lower()
            if choice == '>':
                return {"type": "skip"}
            if choice == '<<':
                return {"type": "exit"}
            if choice in ['1', '2', '3']:
                mode_map = {'1': 'encourage', '2': 'neutral', '3': 'discourage'}
                return {"type": "influence", "mode": mode_map[choice]}
            else:
                print("Invalid choice. (1=Encourage, 2=Neutral, 3=Discourage, >=Next, <<=End)")
