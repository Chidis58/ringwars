import json
import os

class ObservabilityLogger:
    def __init__(self):
        self.daily_decisions = {} # day -> list of decision dicts
        self.all_decisions = []
        self.events = []
        self.history = []

    def log_decision(self, day, connector_id, node_id, cost, personality, reason):
        decision = {
            "day": day,
            "connector_id": connector_id,
            "node_id": node_id,
            "cost": round(cost, 2),
            "personality": personality,
            "reason": reason
        }
        if day not in self.daily_decisions:
            self.daily_decisions[day] = []
        self.daily_decisions[day].append(decision)
        self.all_decisions.append(decision)

    def log_event(self, day, event_type, details):
        event = {
            "day": day,
            "type": event_type,
            **details
        }
        self.events.append(event)

    def log_history(self, day, snapshot):
        self.history.append({"day": day, **snapshot})

    def export_data(self, output_dir, metrics):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # events.log
        with open(os.path.join(output_dir, "events.log"), "w") as f:
            for e in self.events:
                f.write(f"EVENT: {e['type']}\n")
                for k, v in e.items():
                    if k != "type":
                        f.write(f"{k}: {v}\n")
                f.write("\n")

        # metrics.json
        with open(os.path.join(output_dir, "metrics.json"), "w") as f:
            json.dump(metrics, f, indent=4)

        # history.json
        with open(os.path.join(output_dir, "history.json"), "w") as f:
            json.dump(self.history, f, indent=4)

    def get_top_expensive(self, n=10):
        return sorted(self.all_decisions, key=lambda x: x["cost"], reverse=True)[:n]

    def get_influential_trait(self):
        traits = {}
        for d in self.all_decisions:
            reason = d["reason"]
            traits[reason] = traits.get(reason, 0) + 1
        if not traits:
            return "None"
        return max(traits, key=traits.get)
