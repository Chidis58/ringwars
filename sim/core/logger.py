
class Logger:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.logs = []

    def log_day(self, day, events):
        msg = f"--- Day {day} ---"
        if self.verbose:
            print(msg)
            for event in events:
                print(f"  [Event] {event}")
        self.logs.append({"day": day, "events": events})

    def summary(self, connectors, nodes):
        print("\n=== Final Summary ===")
        print("Connectors:")
        for c in connectors.values():
            print(f"  {c}")
        
        print("\nNodes:")
        for n in nodes.values():
            print(f"  {n}")
