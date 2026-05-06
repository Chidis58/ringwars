
def compute_cost(connector, node, overlap, params):
    # Base cost calculation
    cost = params["base_cost"] * (
        1 + overlap * params["overlap_factor"]
    ) * (1 + node.visit_load / params["visit_load_cap"])
    
    # Apply node influence if it exists
    influence = getattr(node, 'influence', 1.0) # 1.0 is neutral
    cost *= influence
    
    return cost
