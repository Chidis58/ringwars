
from sim.experiments.runner import run_experiment
from sim.config import PARAMS, EXPERIMENTS
import json

def main():
    print("=== RingWars Social Mechanics Laboratory ===")
    
    # 1. Baseline Experiment (All flags OFF)
    print("\n[RUNNING] Baseline Experiment...")
    no_experiments = {k: False for k in EXPERIMENTS}
    baseline_res = run_experiment("baseline", PARAMS, seed=42, experiments=no_experiments)
    
    # 2. Chaos Experiment (High Emotional Escalation + Revenge)
    print("\n[RUNNING] Chaos Experiment (Emotional Escalation + Revenge)...")
    chaos_experiments = {
        "revenge_bidding": True,
        "connector_alliances": False,
        "hidden_nodes": False,
        "ring_decay": True,
        "emotional_escalation": True,
    }
    chaos_res = run_experiment("chaos", PARAMS, seed=42, experiments=chaos_experiments)

    # Simple comparison
    print("\n=== LABORATORY COMPARISON ===")
    print(f"Metrics         | Baseline | Chaos")
    print(f"----------------|----------|------")
    print(f"Final Supply    | {baseline_res['total_supply']:>8.1f} | {chaos_res['total_supply']:>5.1f}")
    print(f"Survival Rate   | {baseline_res['survival_rate']*100:>7.1f}% | {chaos_res['survival_rate']*100:>4.1f}%")
    print(f"Avg Visit Load  | {baseline_res['avg_visit_load']:>8.2f} | {chaos_res['avg_visit_load']:>5.2f}")
    
    print("\nSummary reports and raw event logs generated in sim/output/")

if __name__ == "__main__":
    main()
