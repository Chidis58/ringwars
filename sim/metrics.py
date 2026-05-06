import json
import os
from datetime import datetime


def summarize(sim):
    total_supply = sum(c.balance for c in sim.connectors.values())
    total_spent = getattr(sim, "total_spent", 1)

    survival = sum(1 for c in sim.connectors.values() if c.balance > 0)
    survival_rate = survival / len(sim.connectors)

    avg_visit_load = sum(n.visit_load for n in sim.nodes.values()) / len(sim.nodes)

    return {
        "platform_revenue": sim.platform_revenue,
        "burned": sim.total_burned,
        "total_supply": total_supply,
        "burn_rate": sim.total_burned / total_spent,
        "survival_rate": survival_rate,
        "avg_visit_load": avg_visit_load,
    }


def save_results(summary, folder="sim/results"):
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"run_{timestamp}.json")

    with open(path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Saved results → {path}")
