# 💍 RingWars

> A competitive social graph game where status is temporary, strategy is everything, and the economy is alive.

---

## What is this?

RingWars is an **experimental network game** built on a simple premise:

In real social life, attention is scarce, competition is real, and influence has a price. Most apps pretend otherwise. RingWars doesn't.

It models a social graph as a **live competitive economy** — where players spend resources to build connections, defend status, and outmaneuver each other across overlapping social networks. The mechanics are inspired by how status and attention actually work: as contested, dynamic, and driven by social context rather than individual merit alone.

This is **not a dating app.**
It is a **strategy game about social dynamics** — with real stakes, real pressure, and emergent behavior you can't fully predict.

---

## Core Concepts

### The Two Roles

**Connectors** (🔵) are resource managers.
- Hold a token budget (🪙)
- Spend tokens to build and defend connections
- Must navigate social graphs efficiently — overlapping with other Connectors is expensive
- Goal: build high-conviction, defensible connections without depleting capital

**Nodes** (🔴) are attention economists.
- Hold a social pressure score (⤵️)
- Earn tokens by attracting competitive bidding
- Must manage saturation — too much cluster overlap degrades their position
- Goal: maintain healthy diversity, maximize earned value, control who competes for them

Both roles have meaningful agency. Neither is passive.

---

### The Economy

#### 🪙 Tokens
The base currency. Spent by Connectors to initiate connections, compete for Ring status, and defend existing positions. Limited supply forces prioritization.

#### ⤵️ Visit Load (Social Pressure)
Tracks how saturated a Node is with socially-clustered connections.

- **Increases** when Connectors from the same social cluster connect to the same Node
- **Decreases** when the Node maintains diverse, non-overlapping connections

Effects:
- High ⤵️ → future connection costs increase for everyone
- Maximum ⤵️ → temporary lock state (the Node is unreachable until pressure decays)

This mechanic rewards diversity and punishes herd behavior.

#### 💠 Conviction Score
Tracks long-term investment between a Connector and a Node.

- Grows with repeated spending and interactions
- Decays slowly over time
- Prevents "last bid wins" instability — a deeply invested Connector holds structural advantages

#### 💍 Ring Status
The current dominant Connector for a given Node — publicly visible, actively contested.

Awarded to the last Connector who successfully outbids the current threshold. Temporary by design.

---

## Core Mechanics

### Connection Cost

```
cost = base_cost × (1 + cluster_pressure)
```

Cluster pressure activates when a Connector tries to reach a Node already connected to their mutual peers. Low social overlap = cheap. High overlap = expensive. This punishes blind herding and rewards graph exploration.

### Bidding & Escalation

When 💍 changes hands:

```
next_cost = previous_cost × (1 + overlap_factor + streak_factor)
```

- **overlap_factor**: how socially similar the competing Connectors are
- **streak_factor**: how recently and intensely this Node has been contested

This produces escalating bidding wars with natural inflation. Costs rise until someone blinks, runs out of tokens, or finds a smarter play elsewhere.

> **Balance note:** Escalation is soft-capped to prevent runaway inflation locking the economy. Cost growth cannot exceed a percentage of the current average token balance in the active cluster.

### 💍 vs 💠 — Short-term vs Long-term

A Connector with a high 💠 score has *structural* advantages even without holding 💍:

- Lower effective bidding costs
- Faster Conviction recovery after losing Ring status
- Resistance to being fully displaced by a high-spend newcomer

This means brute-force spending is not a guaranteed winning strategy. Patience and consistency compete with aggression.

### Node Influence

Nodes aren't just passive targets. They can actively shape competition:

```
effective_cost = cost × (1 - influence_factor)
```

A Node can reduce perceived cost to invite more competition, encourage specific Connectors, or signal disinterest to cool a bidding war. This is the core of the Node strategy layer.

---

## Information Visibility

Who knows what is a core design variable — not a UX detail.

| Variable | Connector sees | Node sees |
|---|---|---|
| Own 🪙 balance | ✅ | — |
| Other Connectors' 🪙 | ❌ (estimated via behavior) | ❌ |
| Own ⤵️ | — | ✅ |
| Current 💍 holder | ✅ | ✅ |
| 💠 scores | Own only | Aggregate signal |
| Cluster pressure | Partial (own connections) | Full (all inbound) |

Asymmetric information is intentional. Strategy emerges from uncertainty.

---

## Strategy Layers

### Connector Strategies

| Approach | Trade-off |
|---|---|
| **Exploration** — target low-pressure Nodes with no competition | Low cost, low status, high 💠 potential |
| **Competition** — contest high-value Nodes in active clusters | High cost, high status, rapid token burn |
| **Conviction building** — deep investment in one Node over time | Slow, defensible, hard to displace |
| **Disruption** — spike into an active bidding war to drain rivals | Aggressive, zero-sum, expensive |

### Node Strategies

| Approach | Trade-off |
|---|---|
| **Diversity** — accept varied, non-overlapping Connectors | Low ⤵️, healthy economy, lower peak earnings |
| **Auction mode** — encourage cluster competition | High token earnings, rapid ⤵️ buildup, saturation risk |
| **Selective exclusivity** — signal high cost to filter low-conviction bids | Slower competition, higher quality signals |

---

## Public Layer

Beyond the private economy, players can interact publicly through posts, signals, and social proof.

Public activity generates a **Hype Score** that:
- Temporarily reduces perceived connection cost (invites new competition)
- Increases 💠 gain rate for active participants
- Triggers 💍 challenges from previously passive Connectors

The public layer is **psychological pressure**, not core mechanics. It doesn't override the economy — it amplifies it.

---

## Emergent Behavior

The system is designed to produce dynamics that aren't scripted:

- Bidding wars that drain competing Connectors simultaneously
- Nodes engineering their own scarcity
- Social clusters forming and collapsing based on graph topology
- Token economies going inflationary in dense clusters and deflationary in sparse ones
- Long-conviction Connectors outlasting high-spend newcomers

This is the goal. The game is interesting when outcomes surprise everyone, including the designer.

---

## Design Philosophy

RingWars is built on three beliefs:

1. **Honesty over comfort.** Social competition exists. Making it visible and playable is more interesting than pretending it doesn't happen.

2. **Asymmetry is depth.** The two roles are not mirrors of each other. They have different goals, different resources, and different win conditions. That asymmetry is where strategy lives.

3. **Economy first.** Every mechanic must feed back into the token/pressure economy. Features that don't affect the economy don't belong in the core game.

---

## Current Status

RingWars is in **design and simulation phase.**

Active work:
- [ ] Economy simulation (Python / NetworkX) — testing inflation curves, token depletion, cluster dynamics
- [ ] Formula tuning — soft caps, regeneration rates, conviction decay
- [ ] Win condition design — what does "winning" feel like for each role?
- [ ] Minimum viable lobby — what graph density makes the mechanics come alive?

---

## Roadmap

- **v0.1** — Headless simulation: validate economy balance across 500+ cycles
- **v0.2** — CLI prototype: human-playable with text state output
- **v0.3** — Graph visualization: live social graph view, pressure heatmaps, ring ownership history
- **v0.4** — Public layer: posts, hype score, social proof mechanics
- **v1.0** — Full client: multiplayer, real social graph import, AI-populated lobbies for low-density onboarding

---

## Contributing / Feedback

This is an experimental project. The design is not finished. If you have thoughts on:
- Economy balance
- Role asymmetry
- Ethical framing
- Technical architecture

Open an issue or reach out directly. Serious critique welcome.

---

> ⚠️ **Note:** This system intentionally models competitive, ego-driven social dynamics. It is a game about social behavior — not a prescription for it. Balance, fairness, and ethical refinement are ongoing design priorities, not afterthoughts.
