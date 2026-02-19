## Demo 5 — After-Action Replay and Doctrinal Clinic: Learning from the Game

**OODA Phase: Closing the loop — feeding lessons back into future Observe / Orient cycles**

> **Responsible AI & Scope Statement:** This research explores human-AI collaboration and explainable decision-support in fully synthetic, abstract environments. All scenarios, agents, and data are artificially generated. No real-world operational data, contingency plans, systems, or intelligence are used or represented. The prototype is intended exclusively for research, educational, and experimental purposes and does not constitute an operational model, validated planning tool, or source of decision authority. Doctrinal references are inspired by publicly available concepts and do not represent authoritative U.S. Navy doctrine.

### Problem It Solves

After a wargame concludes, the most valuable learning happens during the after-action review (AAR) — but AARs are labor-intensive, depend heavily on facilitator skill, and rarely connect specific in-game decisions back to the doctrinal principles, procedural concepts, or lessons from prior exercises that informed them. Critical decision points get buried in narrative retelling. Participants leave with a subjective sense of what happened rather than a structured understanding of *why* the outcome unfolded as it did, *which doctrinal principles were tested*, and *what would have happened if a different choice had been made*. The institutional knowledge that should flow from wargames into further analysis, discussion, and training is lost or diluted.

### Purpose of the Demo

Given a completed game log — from any of the preceding demos or from a hand-crafted scenario transcript — a team of agents automatically reconstructs the decision timeline, identifies pivotal turning points, evaluates each key decision against an abstracted doctrinal knowledge base, and produces a structured AAR report with "lessons observed." The human user then drives an interactive interrogation: selecting decision points to examine in depth, asking "what if I had done X at turn 3?", and watching agents generate counterfactual branches on the spot using the same engine from Demo 4. This demo completes the narrative arc of the suite: Demos 1–3 *play* the game at increasing complexity; Demo 4 *challenges reasoning*; Demo 5 *supports structured institutional reflection*. For maximum conference impact, the presenter runs Demo 2 (Gray-Zone Escalation), then pipes that game log directly into Demo 5 and the AAR agents analyze what just happened live.

All scenario content is **fully synthetic**. All agent outputs are recommendations and analysis for human review — never directives, orders, or commands.

### What It Illustrates (Multi-Agent)

- **Replay Narrator Agent** ingests the full game log and reconstructs a chronological decision narrative. It identifies the 3–5 most consequential decision points — moments where the outcome pivoted or the decision-maker faced maximum uncertainty — using a simple heuristic: which decisions most changed the distribution of possible outcomes in subsequent turns?

- **Doctrinal Critic Agent** evaluates each identified decision point against an abstracted doctrinal knowledge base provided as text in the notebook — principles inspired by publicly available naval warfare concepts, ROE frameworks, and gray-zone operations literature. It produces a structured assessment: which principles appear relevant, whether the decision appears consistent, whether deviation appears justified given the circumstances, and what doctrinal gap (if any) the decision may expose. This transforms the AAR from anecdotal retelling into structured, traceable analysis — while remaining a research prototype that does not represent authoritative doctrine.

- **Counterfactual Branch Agent** reuses and extends the counterfactual engine from Demo 4, creating a deliberate cross-demo technical connection. The user selects any identified decision point and asks "what if?" The agent perturbs the decision, propagates the change forward through the remaining turns, and produces an alternate outcome with a narrative of how the scenario would have diverged.

- **Lessons Learned Compiler Agent** synthesizes the Narrator's timeline, the Critic's doctrinal assessments, and any counterfactual branches the user explored into a final "Lessons Observed" document structured in a format familiar to military professionals: Observation (what happened), Discussion (why it matters and what the principles suggest), Recommendation (what to consider differently), and Implication for Training (how to incorporate this into future exercises).

- **Explainability Agent** produces transparent, inspectable reasoning traces explaining how and why each AAR agent reached its conclusions. It identifies key interpretive judgments, confidence levels, potential biases, and areas requiring human expert review — ensuring the entire analysis pipeline is auditable and not treated as a black box.

- **Interactive Facilitator / Human-in-the-Loop** — The user, playing the role of the exercise director or a participating commander, drives the AAR by selecting which decision points to examine and which counterfactual branches to explore. The system adapts its analysis to the user's focus rather than dumping a fixed report, modeling the interactive facilitation style of a skilled AAR leader. The user can also ask open-ended questions ("Was there a point where we could have de-escalated without losing deterrent posture?") and the agents search the game log for relevant moments. All decisions remain with the human operator; the system provides analysis and options, not directives.

