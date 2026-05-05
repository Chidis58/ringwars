# 💍 RingWars — System Design

> A competitive social graph game where status is temporary, strategy is everything, and the economy is alive.

---

## 🧠 Overview

RingWars models social interaction as a **dynamic, competitive economy** rather than a passive matching system.

Players operate in a shared network where:
- attention is scarce
- competition is visible
- outcomes are influenced by both strategy and social context

The system is intentionally designed to produce:
- tension
- uncertainty
- emergent behavior

---

## 🎯 Design Goals

### 1. Make Competition Explicit
Traditional platforms hide competition.  
RingWars makes it:
- visible
- measurable
- actionable

---

### 2. Reward Strategy Over Randomness
Success should come from:
- understanding network structure
- managing resources
- timing decisions

Not just chance or volume.

---

### 3. Enable Emergent Behavior
The system should produce:
- bidding wars
- dominance cycles
- cluster formation and collapse

These are not scripted—they emerge from interactions.

---

### 4. Balance Stability and Chaos
Players should be able to:
- play safely and strategically  
**or**
- engage in high-risk, high-reward competition

The system does not force either path.

---

## 🧩 Core Roles

### 🔵 Connectors
Resource-driven agents.

- Hold 🪙 (tokens)
- Spend to form and defend connections
- Navigate social clusters efficiently

**Core tension**
- Expand vs compete
- Efficiency vs dominance

---

### 🔴 Nodes
Attention-driven agents.

- Hold ⤵️ (visit load / pressure)
- Earn 🪙 through competition
- Manage saturation and diversity

**Core tension**
- Maximize earnings vs maintain desirability
- Encourage competition vs avoid burnout

---

## ⚙️ Core Mechanics

### 🪙 Token Economy
- Medium of exchange
- Drives all meaningful interactions
- Limited supply → forces prioritization

---

### ⤵️ Visit Load (Social Pressure)
Represents how saturated a Node is.

- Increases with clustered connections
- Decreases with diversity and inactivity

**Effects**
- Influences future costs
- Impacts Node desirability

---

### 💠 Conviction
Represents long-term investment between a Connector and Node.

- Builds over time through interaction
- Decays slowly

**Purpose**
- Stabilizes relationships
- Prevents pure “last move wins”

---

### 💍 Ring Status
Indicates the current dominant Connector for a Node.

- Changes through competitive bidding
- Public and temporary

**Purpose**
- Drives competition
- Creates visible status

---

## 🔁 Core Loop
Acquire 🪙 → Spend on Nodes → Trigger competition
→ Escalate bids → Earn / Burn tokens
→ Adjust ⤵️ → Shift desirability → Repeat
---

## 🌐 Social Graph Dynamics

The system operates on a network where:

- Nodes and Connectors form connections
- Overlap between connections increases cost
- Clusters naturally emerge

### Key Effects

#### 1. Cluster Pressure
- High overlap → higher costs
- Encourages exploration

#### 2. Scarcity Formation
- Low ⤵️ Nodes become high-value targets

#### 3. Network Strategy
- Position in graph matters as much as resources

---

## ⚖️ System Balance

RingWars maintains balance through:

### Economic Controls
- token burn
- cost scaling
- bid caps

### Behavioral Incentives
- diversity rewards
- saturation penalties

### Structural Limits
- soft matchmaking
- onboarding protection layers

---

## 🎮 Player Experience Layers

### 1. Learning Layer
- sandbox environment
- reduced penalties

### 2. Competitive Layer
- real players
- controlled risk

### 3. Open Economy
- full system exposure
- unrestricted interaction

---

## 💰 Economy Integration

The economy is not an add-on—it is the core system.

- Connectors fund the economy via 🪙 purchases
- Nodes earn through participation
- Platform extracts value through transaction cuts

See: `economy.md`

---

## 🛡️ Onboarding Philosophy

New users must:
- understand the system before facing full risk
- experience both success and failure early

See: `onboarding.md`

---

## 🔥 Emergent Outcomes

When functioning correctly, the system produces:

- bidding wars
- rapid shifts in dominance
- strategic avoidance of crowded clusters
- resource depletion and recovery cycles

These outcomes are:
- unpredictable
- player-driven
- essential to engagement

---

## ⚠️ Design Constraints

### 1. Avoid Pure Pay-to-Win
- diminishing returns
- structural advantages for strategy

---

### 2. Prevent Economic Collapse
- controlled inflation
- burn mechanisms

---

### 3. Maintain Player Agency
- no forced outcomes
- consequences tied to decisions

---

### 4. Ensure Sustainability
- retention loops
- fair earning structure
- balanced incentives

---

## 🧠 Design Philosophy

### Honesty Over Illusion
Competition exists. The system makes it visible.

---

### Asymmetry Creates Depth
Different roles → different strategies → richer interactions.

---

### Economy is Gameplay
Every mechanic feeds back into the economy.

---

### Understanding Drives Retention
Players stay when they understand outcomes—even losses.

---

## 🚀 Current Focus

- Economy simulation (`/sim`)
- Formula tuning
- Onboarding validation
- Core loop stability

---

## 🧩 Summary

RingWars is not a traditional social platform.

It is:
- a competitive system
- a dynamic economy
- a network strategy game

Where:
- status is temporary
- resources are limited
- outcomes emerge from interaction
- 
