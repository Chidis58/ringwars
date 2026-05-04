# 💍 RingWars

An experimental social game exploring competitive relationship dynamics using tokens, social graphs, and psychological pressure.

---

## 🧠 Concept

RingWars is a **network-driven social interaction game** where:

- Boys (B) compete for influence and status
- Girls (G) manage attention, exclusivity, and value
- Social overlap increases cost and tension
- Ownership is temporary, contested, and emotional

This is **not a traditional dating app**.  
It is a **competitive attention economy with strategy, ego, and chaos**.

---

## 🎮 Core Entities

### 👦 Boy (B)
- Has: 🪙 (tokens)
- Goal:
  - Acquire 💍 (ring status)
  - Build unique, non-overlapping connections
  - Outcompete other boys efficiently

---

### 👧 Girl (G)
- Has: ⤵️ (Visit Load / Social Pressure)
- Goal:
  - Earn 🪙
  - Maintain low ⤵️ (avoid saturation)
  - Attract high-value competition

---

## 💰 Core Variables

### 🪙 Tokens
- Currency used by boys
- Spent to:
  - Connect
  - Compete
  - Defend 💍
- Limited → forces strategic decisions

---

### ⤵️ Visit Load (Social Saturation)
Represents how overwhelmed or socially clustered a girl is.

- Increases when:
  - Boys from the same social circle connect to her

- Decreases when:
  - She connects to diverse, unrelated boys
  - She avoids over-engagement

**Effects:**
- High ⤵️ → higher future costs
- Very high ⤵️ → reduced attractiveness or temporary lock

---

### 💠 Conviction Score
Represents how strongly a boy has invested in a girl.

- Increases from:
  - 🪙 spent
  - repeated interactions

- Decays slowly over time

**Purpose:**
- Tracks long-term commitment
- Prevents “last move wins” instability

---

### 💍 Ring (Champion Status)
Represents the **current dominant holder** of a girl.

- Awarded to:
  > The last boy who successfully outbids the current threshold

- Temporary and highly contestable

---

## ⚙️ Core Mechanics

### 🔗 Connecting to a Girl

Cost depends on social overlap:
cost = Base x ( 1 Cluster Pressure)
- Low overlap → cheap, efficient
- High overlap → expensive, competitive

---

### 🔥 Cluster Pressure

Triggered when:
- A boy tries to connect to a girl already connected to his mutual friends

Effects:
- 🪙 Cost increases
- ⤵️ increases (bad for girl)

---

### 💍 Buyback / Bidding System

Each time 💍 changes hands:
Next Cost = Previous Cost x ( 1 + overlap + streak)
- Overlap = social graph similarity
- Streak = recent competition intensity

**Result:**
- Escalating bidding wars
- Emotional decision-making
- Rapid cost inflation

---

### 💠 vs 💍 Dynamic

- 💍 = current winner (short-term)
- 💠 = true investment (long-term)

A boy can:
- Win 💍 quickly with high spending
- Lose later to someone with stronger 💠

---

## 👧 Girl Strategy Layer

Girls balance:

| Choice | Outcome |
|------|--------|
| Accept diverse boys | ⤵️ decreases (healthy) |
| Accept clustered boys | ⤵️ increases (risky) |
| Encourage bidding | more 🪙, more chaos |

---

### 🎭 Influence Mechanic

Girls can influence boys by:
- Encouraging competition
- Creating urgency
- Reducing perceived cost
Effective Cost = Cost x (1 - InfluenceFactor)
---

## 👦 Boy Strategy Layer

Boys must choose between:

- **Exploration**
  - Find new girls (low cost, low competition)

- **Competition**
  - Fight for existing girls (high cost, high status)

---

## 🌍 Public vs Private Layers

### 🔒 Private Layer (Core Game)
- All real mechanics happen here
- 💍, 💠, 🪙, ⤵️ are calculated here

---

### 🌐 Public Layer (Optional Feature)

Triggered by posts:
- Appeals
- Flirting
- Social proof
- Drama

Public engagement creates:

### 📈 Hype Score
- Increases 💠 gain rate
- Encourages 💍 challenges
- Reduces perceived cost temporarily

**Role:**
> Public = psychological pressure layer, not core logic

---

## 🔁 Emergent Dynamics

- Bidding wars between boys
- Strategic girls controlling attention flow
- Social graph-based pricing
- Resource depletion and risky plays
- High-value vs over-saturated players

---

## 🎯 Design Philosophy

This system is designed to be:

- Competitive
- Emotional
- Unstable (in a controlled way)
- Socially reactive

It intentionally introduces:
- Ego
- Scarcity
- Pressure
- Strategy

---

## 🚧 Future Ideas

- Time-based decay systems
- AI-driven influence behavior
- Reputation scoring
- Group dynamics (girl clusters affecting each other)
- Visualization of social graphs

---

## ⚠️ Note

This is an experimental system exploring social dynamics.  
Balance, fairness, and ethical considerations will need refinement as the system evolves.

---

## 🚀 Goal

To create a **non-traditional social interaction system** that is:
- Engaging
- Strategic
- Dramatic
- Worth talking about
