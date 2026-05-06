
from sim.experiments.runner import run_experiment
from sim.config import PARAMS
import json

def main():
    print("=== RingWars Experimental Runner ===")
    
    # Define experiments
    # 1. Baseline
    print("\nRunning Baseline Experiment...")
    baseline_res = run_experiment("baseline", PARAMS, seed=42)
    print(f"  Seed: {baseline_res['seed']}")
    print(f"  Supply: {baseline_res['total_supply']:.1f}")
    print(f"  Survival: {baseline_res['survival_rate']*100:.1f}%")
    
    obs = baseline_res.get("observability", {})
    print(f"  Most Influential Trait: {obs.get('most_influential_trait')}")
    print(f"  Top Expensive Decision: {obs.get('top_expensive_decisions')[0] if obs.get('top_expensive_decisions') else 'N/A'}")

    # 2. Reproduction Check (Same seed)
    print("\nRunning Reproduction Check (Seed 42)...")
    repro_res = run_experiment("repro", PARAMS, seed=42)
    
    if baseline_res['total_supply'] == repro_res['total_supply']:
        print("  SUCCESS: Simulation is deterministic and reproducible.")
    else:
        print("  FAILURE: Determinism broken.")
        print(f"  Diff: {repro_res['total_supply'] - baseline_res['total_supply']}")

if __name__ == "__main__":
    main()
