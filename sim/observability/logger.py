
class ObservabilityLogger:
    def __init__(self):
        self.daily_decisions = {} # day -> list of decision dicts
        self.all_decisions = []

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
