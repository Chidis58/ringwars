# 💰 RingWars Economy Model

> A token-driven competitive economy where spending, scarcity, and social pressure shape outcomes.

---

## 🪙 Token Supply & Pricing

### Purchase Packs

| Pack | Price | 🪙 Amount | Bonus | Effective Rate |
|------|------|----------|------|----------------|
| Small | $4.99 | 500 | — | 100 🪙 / $ |
| Medium | $19.99 | 2,200 | +10% | 110 🪙 / $ |
| Large | $49.99 | 6,000 | +20% | 120 🪙 / $ |

**Design Intent**
- Encourage larger purchases without forcing them
- Anchor perceived value of 🪙

---

## 🔁 Core Spend Loop

### Connection Attempt
Base cost = 10 🪙
**Distribution**
- 70% → Node
- 20% → Platform
- 10% → Burn

---

### 💍 Bidding / Buyback
Next Price = P × (1 + overlap + streak)
**Distribution**
- 60% → Node
- 25% → Platform
- 15% → Burn

**Design Intent**
- High emotional spending → higher platform cut
- Drives core monetization

---

### 🧨 Overcommit (Debt Mechanic)
Repayment = borrowed × 1.25
**Penalty Split**
- 15% → Platform
- 10% → Burn

**Design Intent**
- Enables aggressive plays
- Punishes reckless behavior

---

## 🔥 Inflation Control

### Burn Target
25–35% of total spent 🪙 should be burned
**Sources**
- Connection burn
- Bid burn
- Debt penalties

---

### Dynamic Cost Cap

max_bid ≤ 20% of avg_cluster_balance
**Prevents**
- Whale dominance
- Economic breakage

---

### ⤵️ Visit Load Multiplier
effective_cost = base_cost × (1 + ⤵️ / cap)
**Effect**
- High saturation → higher costs
- Natural inflation regulator

---

## 💸 Node Earnings

### Earnings Sources
- Connection attempts
- Bidding wars

---

### Conversion
1000 🪙 ≈ $7
**Design Intent**
- Maintain platform margin
- Prevent direct arbitrage

---

### Withdrawal Rules
- 10% fee
- 24–72 hour cooldown

---

### Tiered Earnings (Behavior Control)

| ⤵️ Level | Payout Rate |
|----------|------------|
| Low | 100% |
| Medium | 85% |
| High | 60% |

**Effect**
- Encourages diversity
- Discourages clustering

---

## 🎯 Connector Economy Pressure

### Daily Regen
+50 🪙 / day
**Purpose**
- Retention for non-paying users

---

### Loss Recovery

If >40% loss:
- Next 3 actions → 30% discount

---

## 🏦 Revenue Summary

From every 100 🪙 spent:

- 60–70 → Nodes
- 20–25 → Platform
- 15–25 → Burn

---

## ⚖️ Anti-Whale Mechanics
effective_power = spend × (1 / log(n+1))
**Effect**
- Diminishing returns on repeated bids
- Prevents brute-force dominance

---

## 📊 Key Metrics

### Economy
- Total 🪙 supply
- Burn %
- Spend per session

### Player
- New user survival rate
- % winning 💍
- Avg remaining 🪙

### Node
- Avg ⤵️
- % locked Nodes

---

## 🧩 Core Loop
Buy 🪙 → Spend → Compete → Escalate
→ Platform takes cut → Burn reduces supply
→ Nodes earn → Withdraw → ⤵️ regulates demand
---

## ⚠️ Notes

- System is sensitive to inflation
- Requires constant tuning
- Must include spending safeguards

---

## Philosophy

> The economy is the game.  
> If the economy breaks, the game breaks.
