
import json
import os
from ..core.engine import Simulation
from ..scenarios.default import create_world

def run_experiment(name, config, seed=None):
    """
    Runs a single experiment with a given name, config (params), and seed.
    """
    exp_seed = seed if seed is not None else config.get("seed", 42)
    
    # Initialize world
    connectors, nodes = create_world(
        n_connectors=config.get("n_connectors", 20),
        n_nodes=config.get("n_nodes", 20),
        seed=exp_seed
    )
    
    # Run simulation
    sim = Simulation(connectors, nodes, config, verbose=False, seed=exp_seed)
    sim.run(days=config.get("days", 30))
    
    # Collect results
    final_snapshot = sim.history[-1]
    
    # Top winners (connectors with most balance)
    winners = sorted(
        [{"id": c.id, "balance": c.balance} for c in sim.connectors.values()],
        key=lambda x: x["balance"],
        reverse=True
    )[:5]
    
    # Top nodes (nodes with most earnings)
    top_nodes = sorted(
        [{"id": n.id, "earnings": n.earnings} for n in sim.nodes.values()],
        key=lambda x: x["earnings"],
        reverse=True
    )[:5]
    
    result = {
        "experiment_name": name,
        "seed": exp_seed,
        "total_supply": final_snapshot["supply"],
        "platform_revenue": final_snapshot["revenue"],
        "burned": final_snapshot["burned"],
        "avg_visit_load": final_snapshot["avg_visit_load"],
        "survival_rate": final_snapshot["survival_rate"],
        "winner_connectors": winners,
        "top_nodes": top_nodes
    }
    
    # Save to results/
    os.makedirs("sim/results", exist_ok=True)
    file_path = f"sim/results/{name}_s{exp_seed}.json"
    with open(file_path, "w") as f:
        json.dump(result, f, indent=2)
    
    return result

def run_multiple_experiments(experiments_list):
    """
    experiments_list: list of (name, config, seed)
    """
    results = []
    for name, config, seed in experiments_list:
        results.append(run_experiment(name, config, seed))
    return results
