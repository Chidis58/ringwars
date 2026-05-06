
def compute_cost(connector, node, overlap, params):
    cost = params["base_cost"] * (
        1 + overlap * params["overlap_factor"]
    ) * (1 + node.visit_load / params["visit_load_cap"])
    return cost
