# 📊 RingWars Metrics Framework

> Defines how system health, player behavior, and economic stability are measured in both simulation and production.

---

## 🧠 Purpose

Metrics are used to answer three critical questions:

1. **Is the economy stable?**
2. **Are players surviving and engaging?**
3. **Is the platform generating sustainable revenue?**

---

## 🧩 Metric Categories

1. Economy Health
2. Player Health
3. Node Health
4. Competition Dynamics
5. Platform Revenue
6. Risk & Safety Signals

---

## 💰 1. Economy Health

### Total Supply

total_supply = sum(all connector balances)

Tracks inflation/deflation.

---

### Burn Rate

burn_rate = total_burned / total_spent

**Target:** 25–35%

- Too low → inflation risk  
- Too high → player starvation  

---

### Token Velocity

velocity = total_spent / total_supply

Measures how active the economy is.

---

### Avg Balance

avg_balance = total_supply / num_connectors

Used for:
- bid caps
- inflation control

---

## 👤 2. Player Health (Connectors)

### Survival Rate

survival_rate = % of connectors with balance > threshold

**Target:** >70%

---

### First Session Success

- % of players who:
  - win ≥1 💍
  - retain ≥30% of starting 🪙

---

### Bankruptcy Rate

bankrupt = % of connectors with balance <= 0

**Target:** <20%

---

### Spend Distribution

- median spend
- top 10% spend share

Detects whale dominance.

---

## 🔴 3. Node Health

### Avg ⤵️ (Visit Load)

avg_visit_load = mean(node.visit_load)

---

### Distribution

Track % of Nodes in:

- Low ⤵️ (healthy)
- Mid ⤵️ (active)
- High ⤵️ (saturated)
- Locked (unusable)

---

### Earnings Distribution

- median earnings
- top 10% share

Detects inequality or exploitation patterns.

---

## 💍 4. Competition Dynamics

### Ring Turnover Rate

turnover = number of 💍 changes per tick

- Too low → stale system  
- Too high → chaotic/no stability  

---

### Avg Bid Escalation

avg_next_price / avg_previous_price

Measures intensity of bidding wars.

---

### Cluster Pressure Index

avg_overlap across all interactions

Indicates:
- exploration vs crowding behavior

---

## 🏦 5. Platform Revenue

### Total Revenue

platform_revenue

---

### Revenue per Tick

revenue / ticks

---

### ARPU (Simulation Approx)

avg_revenue_per_connector

---

### Revenue Source Split

- % from:
  - connections
  - bids
  - debt penalties

---

## ⚠️ 6. Risk & Safety Signals

### Whale Dominance

top_10_percent_balance_share

**Alert if:** >50%

---

### Node Saturation Risk

% nodes with ⤵️ > cap * 0.8

---

### Player Churn Risk (Simulated)

Proxy signals:
- repeated low balance
- inactivity after loss
- failed bid streaks

---

## 🧪 Simulation vs Production

### In Simulation
- All metrics available
- Used for tuning parameters

---

### In Production
Track:
- aggregated + anonymized data
- session-level behavior
- retention (Day 1, Day 7, Day 30)

---

## 🧩 Minimal Metric Set (v0.1)

If you want to start simple, track:

- total_supply
- burn_rate
- survival_rate
- avg_visit_load
- platform_revenue
- ring_turnover

---

## 🧠 Interpretation Guide

| Signal | Meaning | Action |
|------|--------|-------|
| High supply + low burn | Inflation | Increase burn |
| Low survival | Too punishing | Add recovery |
| High ⤵️ everywhere | Overcrowding | Encourage exploration |
| Low turnover | Stagnation | Boost incentives |
| High whale share | Pay-to-win | Add caps |

---

## 🚀 Evolution

Metrics should evolve with the system:

- v0.1 → basic economy tracking  
- v0.2 → behavior + clustering  
- v0.3 → predictive signals (churn, collapse)

---

## Philosophy

> If you can't measure it, you can't tune it.  
> If you can't tune it, the system will drift—and eventually break.


---
