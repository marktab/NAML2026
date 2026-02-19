## Demo 4 — Counterfactual COA Analysis

**OODA Phase: Orient / Decide (stress-testing the boundary)**

> **Responsible AI & Scope Statement:** This research explores human-AI collaboration and explainable decision-support in fully synthetic, abstract environments. All scenarios, agents, and data are artificially generated. No real-world operational data, contingency plans, systems, or intelligence are used or represented. The prototype is intended exclusively for research, educational, and experimental purposes and does not constitute an operational model, validated planning tool, or source of decision authority.

### Problem It Solves

Human feedback in wargaming — and in AI-assisted decision-making more broadly — can unintentionally reward biased or brittle patterns. A planner might consistently prefer escalation because it "feels decisive," anchor on a favorite approach regardless of conditions, mirror the last successful method without testing whether it generalizes, or reject a valid COA because of recency bias. These cognitive biases are well-documented in decision-science research (and explicitly flagged in the Vasankari NPS thesis, 2024, which argues that decision-support systems should oppose planner bias by producing alternatives "without the subjective, cultural mindset") but are almost never surfaced or challenged in real time during an exercise. The result is that AI systems guided by human feedback can inherit and amplify these biases.

### Purpose of the Demo

Demonstrate counterfactual augmentation and explanation in a fully synthetic, research-only environment: when a user accepts or rejects a proposed course of action, the system generates "nearby worlds" — scenarios that differ from the current one by a single assumption — and tests whether the user's preference would still hold under those small perturbations. If the preference is inconsistent across similar worlds, the system identifies the likely cognitive bias by name and presents an "appeal brief" explaining what changed, what stayed constant, and why the recommendation does or doesn't remain valid. This is the most novel demo in the suite relative to the existing literature, directly embodying the abstract's emphasis on counterfactual reasoning and bias exposure. Placing it after the Hierarchy demo (Demo 3) ensures the audience has seen enough game-play to appreciate what is being stress-tested. All agent outputs are recommendations and analysis — never orders or directives.

### What It Illustrates (Multi-Agent)

- **COA Generator Agent** suggests 2–3 courses of action for a given synthetic tactical situation, each with a brief rationale, estimated risk, and resource requirements. The COAs represent meaningfully different approaches (e.g., aggressive vs. deliberate vs. indirect) so that preference patterns are detectable. All outputs are advisory; final decisions remain with the human operator.

- **Counterfactual Perturbation Agent** systematically varies one assumption at a time — weather, unit readiness, adversary intent, ROE constraints, comms reliability, alliance posture — and re-presents the same COA set in the perturbed world. It generates 3–5 "nearby worlds" per decision point, each differing by exactly one variable so that causal attribution is unambiguous.

- **Bias / Feedback Auditor Agent** compares the user's accept/reject decisions across the original and perturbed worlds. When it detects inconsistency (e.g., the user accepts COA A in the baseline but rejects A in a near-identical world where only weather changed), it labels the likely cognitive bias by name: anchoring, recency bias, escalation commitment, mirror-imaging, or availability heuristic. The named-bias labeling is what elevates this from a prototype to a research instrument that practitioners familiar with red-teaming concepts will recognize.

- **Explainability Agent** produces a structured "appeal brief" for each flagged inconsistency: what assumption changed between the worlds, what stayed constant, how the COA's expected outcome shifted (or didn't), and a recommendation on whether the original preference should be reconsidered. This is the most detailed explainability output in the suite.

- **Adjudication Agent** provides an outcome score for each COA in each world using a simple, transparent rule-based evaluation. The scoring rubric is published in the notebook so reviewers can verify the adjudication is not a black box — directly addressing the literature's concern about LLM explainability and trust.

- **Planner-in-the-Loop Interaction** — The user provides accept/reject feedback interactively, making the bias detection feel personal and informative. This is the strongest audience engagement moment in the demo suite: the presenter can invite an audience member to make the choices and then watch the system surface their own reasoning patterns for reflection and learning. All decisions remain with the human operator throughout.

### Synthetic Data Notice

All scenario content — including locations, force compositions, timelines, and tactical parameters — is fully fictional and synthetically generated. No real-world operational data, contingency plans, intelligence products, unit designations, or classified material are used or referenced. The scenario is inspired by publicly available, abstracted military decision-making frameworks for research and educational purposes only.
