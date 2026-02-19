## Demo 2 — Maritime Gray-Zone Escalation Analysis Sandbox: Red / Blue / White Cell Play

**OODA Phase: Orient / Decide / Act**

> **Responsible AI & Scope Statement:** This research explores human-AI collaboration and explainable decision-support in fully synthetic, abstract environments. All scenarios, agents, and data are artificially generated. No real-world operational data, contingency plans, systems, or intelligence are used or represented. The prototype is intended exclusively for research, educational, and experimental purposes and does not constitute an operational model, validated planning tool, or source of decision authority.

### Problem It Solves

Gray-zone encounters — contested transits, provocative maritime maneuvers, ambiguous use of militia vessels, electronic interference below the threshold of armed conflict — create rapid escalation risk where the wrong response can trigger an international incident and the right response requires balancing deterrence, de-escalation, mission continuation, legal constraints, and strategic communication simultaneously. No single staff officer holds all these competing equities, and current wargaming tools rarely model the information-warfare and legal dimensions alongside the kinetic ones.

### Purpose of the Demo

Simulate a multi-turn gray-zone maritime encounter using fully synthetic, fictional scenarios where Red, Blue, and White cell agents play against each other across turns. The system tracks escalation, strategic messaging, legal compliance, and operational objectives using quantified scoring dimensions — inspired by the NATO STO-MP-SAS-192 card-based wargame approach (Meltschack & Weller, German Armed Forces) — and recommends actions with explicit risk tradeoffs at each decision point. All agent outputs are recommendations and analysis, never orders or directives. This demo produces a game log that Demo 5 (After-Action Review) can consume directly, enabling a live chain during the conference presentation.

### What It Illustrates (Multi-Agent)

- **Blue Planner Agent** selects actions from a defined menu each turn: shadowing posture, maneuver changes, hail-and-warn, ISR reposition, EMCON adjustments, or public affairs messaging. Each action carries explicit scores across five dimensions — Impact, Escalation, Communication, Political, and Resource — displayed as a running dashboard visible to the audience.

- **Red Team Agent** selects provocations from its own menu: unsafe intercept, AIS spoofing, militia vessel deployment, directed-energy harassment, jamming bursts, or disinformation release. After each turn, the Red agent explains its reasoning, creating a transparent adversary thought process the audience can evaluate and challenge.

- **White Cell / Umpire Agent** adjudicates outcomes and updates escalation indices using a simple, published rule set (shown in the notebook). It resolves interactions between Red and Blue actions, advances the scenario clock, and announces threshold crossings (e.g., escalation moving from "posturing" to "crisis").

- **Legal / ROE Agent** constrains Blue's available actions each turn based on the current ROE posture and escalation level. When an action is prohibited, it explains why; when an action is permitted but carries legal exposure, it flags the risk. This constraint layer is not present in the NATO precedent and illustrates how legal-advisor integration, inspired by publicly available doctrinal concepts, could function in an abstract wargaming environment.

- **Strategic Communications Agent** drafts a short public statement for Blue each turn and predicts the likely adversary media response and information-environment effect. This illustrates the information-warfare dimension underrepresented in the current wargaming AI literature and shows the audience something they rarely see modeled.

- **Explainability Agent** produces transparent, inspectable reasoning traces after each turn. It summarizes the causal chain of agent decisions, identifies potential cognitive biases (anchoring, recency bias, escalation commitment, mirror-imaging, availability heuristic), highlights critical decision points, and verifies that all agent outputs remained within the scope of recommendations and analysis — not directives. This agent satisfies the Responsible AI requirement that every demo include a dedicated explainability pathway.

