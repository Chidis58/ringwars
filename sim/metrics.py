def summarize(sim):
    total_supply = sum(c.balance for c in sim.connectors.values())
    avg_visit_load = sum(n.visit_load for n in sim.nodes.values()) / len(sim.nodes)

    return {
        "platform_revenue": sim.platform_revenue,
        "burned": sim.total_burned,
        "total_supply": total_supply,
        "avg_visit_load": avg_visit_load,
    }
