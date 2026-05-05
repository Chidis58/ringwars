def summarize(sim):
    total_supply = sum(c.balance for c in sim.connectors.values())
    total_spent = sim.total_spent if hasattr(sim, "total_spent") else 1

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
