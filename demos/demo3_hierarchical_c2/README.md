## Demo 3 — Hierarchical Decision-Flow Simulation

**OODA Phase: Decide / Act (across echelons)**

> **Responsible AI & Scope Statement:** *This research explores human-AI collaboration and explainable decision-support in fully synthetic, abstract environments. All scenarios, agents, and data are artificially generated. No real-world operational data, contingency plans, systems, or intelligence are used or represented. The prototype is intended exclusively for research, educational, and experimental purposes and does not constitute an operational model, validated planning tool, or source of decision authority.*

### Problem It Solves

Single-agent AI approaches struggle to scale decision-making across multiple echelons in complex operational environments. A commander sets strategic intent, warfare managers propose force allocations and synchronized plans, and unit-level operators carry out tactical actions — each operating at a different level of abstraction, time horizon, and information granularity. Flattening this into a single AI agent either overwhelms the model with irrelevant detail or strips away the coordination dynamics that make multi-echelon decision-making hard. The research literature (Boron et al., NPS 2024; Boron et al., I/ITSEC 2023) has demonstrated this hierarchy using reinforcement learning in the Atlatl simulation; this demo re-creates the architecture using LLM agents in AutoGen, showing what happens when RL policies are replaced with natural-language reasoning — a novel bridge between the RL-based and LLM-based wargaming research communities.

### Purpose of the Demo

Run a compact, fully synthetic micro-wargame where decisions decompose across a three-level hierarchy: a Commander sets intent and prioritizes objectives, Managers propose resource allocations and create synchronized sub-plans, and Operators carry out recommended actions on a simple grid. All unit names, locations, and scenario events are fictional and invented for this exercise. The demo is immediately legible to warfighters because it mirrors familiar staff-like structures — Commander → Warfare Managers → Unit Operators. A Multi-Model Selector mechanism visibly chooses between scripted heuristics (for operators in routine situations) and LLM reasoning (for higher-level tradeoffs or novel encounters) at each decision step, demonstrating the hybrid multi-model concept without requiring any model training. All agent outputs are framed as **recommendations and analysis** — never as orders or directives. Final decisions remain with the human operator at all times.

### What It Illustrates (Multi-Agent)

- **Commander Agent** receives a high-level objective (e.g., "control the strait while preserving force") and decomposes it into prioritized sub-objectives with risk tolerance guidance. It operates on a coarse, abstracted view of the battlespace — analogous to the Commander observation abstraction in the Boron HRL framework — and provides recommended intent statements and suggested operating areas to its Managers.

- **Two Manager Agents** (Surface Warfare Manager and Air Warfare Manager) each receive the Commander's recommended intent and a suggested operating area, then create synchronized sub-plans. They propose unit positions, identify resource conflicts through a coordination exchange visible in the agent chat log, and provide recommended actions to their operators.

- **Operator Agents** carry out recommended tactical actions on a text-based grid representation: patrol, screen, intercept (flagged for human confirmation), or conserve. They operate on local information within their assigned area. Their action selection alternates between scripted heuristics (for routine movement) and LLM-generated reasoning (when encountering unexpected contacts or ambiguous recommendations), with the selection logic visible to the audience. Consequential actions such as INTERCEPT require explicit human confirmation before proceeding.

- **Multi-Model Selector Agent** (lightweight coordinator) monitors each decision point and chooses whether to route it to a scripted heuristic or to LLM reasoning based on the complexity and novelty of the situation. A sidebar log shows the audience each selection and the rationale, making the hybrid concept tangible. This directly demonstrates the portability and modularity story from the abstract — the same architecture can swap in different reasoning engines depending on the deployment environment's constraints.

- **Feedback Aggregator** collects outcomes from each turn and surfaces them to the Commander and Manager levels, closing the tactical feedback loop and enabling mid-game adaptation of recommendations — showing that the hierarchy is not purely top-down but responsive to ground truth.

- **Explainability Agent** produces a transparent reasoning trace after each turn, explaining *why* each agent reached its conclusion. It traces the causal chain from Commander intent through Manager plans to Operator outcomes, identifies potential cognitive biases (anchoring, recency bias, escalation commitment, mirror-imaging, availability heuristic), and makes the Multi-Model Selector's routing decisions auditable. This ensures every decision chain terminates in an inspectable explanation.

### Responsible AI Commitments

- **Fully Synthetic Data:** All unit names, locations, scenario events, and force laydowns are entirely fictional. No real-world operational data, intelligence, or military designations are used.
- **Human-in-the-Loop:** Consequential actions (INTERCEPT/engagement) require explicit human confirmation. All agent outputs are recommendations, not orders.
- **Explainability:** A dedicated Explainability Agent produces auditable reasoning traces for every turn. Scoring criteria and decision rationale are visible, never hidden.
- **No Doctrinal Authority:** This demo is inspired by publicly available decision-making frameworks for educational purposes. It does not represent authoritative doctrine, ROE, or operational procedures.
- **Scope Boundary:** This prototype is intended exclusively for research, educational, and experimental purposes and does not constitute an operational model, validated planning tool, or source of decision authority.

