## Demo 1 — "Living Scenario Brief": Adaptive Situational Awareness Under Uncertainty

**OODA Phase: Observe / Orient**

> **Responsible AI & Scope Statement:** This research explores human-AI collaboration and explainable decision-support in fully synthetic, abstract environments. All scenarios, agents, and data are artificially generated. No real-world operational data, contingency plans, systems, or intelligence are used or represented. The prototype is intended exclusively for research, educational, and experimental purposes and does not constitute an operational model, validated planning tool, or source of decision authority.

### Problem It Solves

Operational scenarios are briefed as static snapshots, yet situations evolve continuously with incomplete, delayed, and often contradictory reporting. A commander's understanding of the operational environment can lag reality by hours when the staff must manually reconcile disparate intelligence feeds, flag contradictions, track shifting confidence levels, and re-draft briefings each cycle. There is no lightweight, automated mechanism that fuses fragmented reports and produces a commander-ready update explaining not only *what* the current situation is, but *how and why* it changed.

### Purpose of the Demo

Show a multi-agent scenario-learning loop that maintains a "story world" — a living JSON data structure of events, actors, locations, and uncertainties — and updates it each turn as new simulated intelligence arrives. Each cycle, the system produces a structured SITREP that describes the current assessed situation and explains what evidence drove each assessment change since the last brief. The demo is explicitly structured around the OODA loop (Observe → Orient → Decide → Act), connecting with established military decision-making frameworks and the methodology demonstrated in the LLM wargaming literature (Chen & Chu, CVPRW 2024). This is the most accessible demo in the suite — every warfighter knows what a SITREP is — and it teaches the audience how multi-agent orchestration works before the scenarios grow more complex.

**All scenario content — actors, locations, events, timelines, and data — is entirely synthetic and fictional.** No real-world unit designations, geographic coordinates, weapons systems, classification markings, or operational data are used. Agent outputs are framed as recommendations and analysis, never as orders or directives. All decisions remain with the human operator.

### What It Illustrates (Multi-Agent)

- **Scenario Orchestrator Agent** maintains the authoritative world state as a structured JSON object (timeline of events, actor positions and dispositions, known and unknown variables, current uncertainty flags). It manages turn sequencing and ensures all agents share a consistent, versioned picture. This is the shared data backbone that all five demos reuse.

- **ISR / Intel Fusion Agent** generates simulated intelligence reports each turn — SIGINT intercept snippets, HUMINT source summaries, UAV detection logs, open-source indicators — and flags contradictions or gaps between reports. It injects realistic noise: some reports confirm earlier information, some contradict it, and some introduce entirely new actors or threats. The noise level can be tuned to demonstrate how the system degrades gracefully under information overload. All intelligence is artificially generated; no real intelligence products or formats are replicated.

- **Assessment Agent** updates threat and risk ratings, adjusting confidence levels using a simple Bayesian-inspired heuristic (transparent to the audience). It explicitly tracks which assessments went up or down in confidence and why, maintaining a changelog. This is the Orient phase made visible. The agent recommends and assesses — it does not direct or order.

- **Briefing / Explainer Agent** consumes the updated world state and the assessment changelog to produce a concise SITREP in a structured format: situation summary, key changes since last brief, assessed threat level with confidence, information gaps, and recommended priority information requirements (PIRs). Every assessment is accompanied by a one-sentence evidence citation, supporting transparent and explainable AI reasoning.

- **Human-in-the-Loop Turn** — After each brief, the user (acting as the commander) can ask a clarifying question, challenge an assessment, or inject a commander's critical information requirement. The agents respond and may revise the world state, demonstrating the interactive human-AI collaboration layer central to the abstract. The human retains full decision authority at all times.
