
import json
import sys

def compare_results(path_a, path_b):
    try:
        with open(path_a, 'r') as f:
            a = json.load(f)
        with open(path_b, 'r') as f:
            b = json.load(f)
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    print(f"\n=== Experiment Comparison ===")
    print(f"{'Metric':<20} | {'Exp A':<15} | {'Exp B':<15} | {'Diff':<15}")
    print("-" * 75)

    metrics = [
        ("total_supply", "Supply"),
        ("platform_revenue", "Revenue"),
        ("burned", "Burned"),
        ("avg_visit_load", "Avg Visit Load"),
        ("survival_rate", "Survival Rate")
    ]

    for key, label in metrics:
        val_a = a.get(key, 0)
        val_b = b.get(key, 0)
        diff = val_b - val_a
        pct = (diff / val_a * 100) if val_a != 0 else 0
        print(f"{label:<20} | {val_a:15.2f} | {val_b:15.2f} | {diff:+15.2f} ({pct:+.1f}%)")

    # Winner Shifts
    print("\n--- Winner Shifts (Top 1) ---")
    win_a = a["winner_connectors"][0] if a.get("winner_connectors") else None
    win_b = b["winner_connectors"][0] if b.get("winner_connectors") else None
    print(f"Exp A Winner: C{win_a['id'] if win_a else 'N/A'} (Bal: {win_a['balance'] if win_a else 0:.1f})")
    print(f"Exp B Winner: C{win_b['id'] if win_b else 'N/A'} (Bal: {win_b['balance'] if win_b else 0:.1f})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 -m sim.experiments.compare <path_to_a.json> <path_to_b.json>")
    else:
        compare_results(sys.argv[1], sys.argv[2])
