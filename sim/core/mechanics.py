
def compute_cost(connector, node, overlap, params, experiments=None):
    # Base cost calculation
    cost = params["base_cost"] * (
        1 + overlap * params["overlap_factor"]
    ) * (1 + node.visit_load / params["visit_load_cap"])
    
    # Apply node influence if it exists
    influence = getattr(node, 'influence', 1.0) # 1.0 is neutral
    cost *= influence

    # EXPERIMENT: emotional_escalation
    if experiments and experiments.get("emotional_escalation") and node.streak > 2:
        cost *= (1 + (node.streak - 2) * 0.5) # +50% cost per streak point above 2
    
    return cost
