
class Logger:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.logs = []

    def _fmt_c(self, cid):
        return f"🕺{cid}" if cid is not None else "None"

    def _fmt_n(self, nid):
        return f"💃{nid}" if nid is not None else "None"

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
            print(f"  {self._fmt_c(c.id)} | Balance: 🪙{c.balance:.2f}")
        
        print("\nNodes:")
        for n in nodes.values():
            rh = n.ring_holder
            rh_fmt = self._fmt_c(rh) if rh is not None else "None"
            print(f"  {self._fmt_n(n.id)} | 🤱 {n.visit_load:.1f} | 💍 {rh_fmt}")
