def cluster_overlap(connector, node, connectors):
    overlap = 0
    for other_id in node.connections:
        if other_id == connector.id:
            continue
        overlap += len(connectors[other_id].connections & connector.connections)
    return overlap


def compute_cost(connector, node, overlap, params):
    return params["base_cost"] * (1 + overlap * params["overlap_factor"]) * (
        1 + node.visit_load / params["visit_load_cap"]
    )
