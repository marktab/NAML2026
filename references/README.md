# References

Source documents supporting the accepted abstract:

**"Rapid Prototyping for Naval AI Wargaming: Multi-Agent Scenario Learning and Counterfactual Reasoning with Python and AutoGen"**

---

## File Index

| # | Filename | Short Label |
|---|----------|-------------|
| 1 | `2408_13333v1.pdf` | Black (NPS 2024) — HRL Dissertation |
| 2 | `2402_06694v1.pdf` | Black et al. (I/ITSEC 2023) — HRL Conference Paper |
| 3 | `Large_Language_Models_in_Wargaming_Methodology_Application_and_Robustness.pdf` | Chen & Chu (CVPRW 2024) — LLM Wargaming |
| 4 | `MPSAS19214P.pdf` | Meltschack & Weller (NATO STO 2024) — LLM-Enhanced Card Wargame |
| 5 | `master_Vasankari_Lauri_2024.pdf` | Vasankari (Aalto/NPS 2024) — MARL for Littoral Warfare |
| 6 | `applsci0901089.pdf` | Han et al. (Applied Sciences 2019) — Multi-Agent USV Training |

---

## Responsible AI Lens for the Literature

Every reference in this collection was selected and is read through the project's five Responsible AI constraints. When evaluating findings, adapting architectures, or citing results from these papers, the following principles apply:

| Responsible AI Principle | How It Shapes Our Reading of the Literature |
|---|---|
| **Fully Synthetic Data Only** | No reference contributes real operational data. Architectures and methods from these papers are adopted in purely synthetic, fictional scenarios. Real-world system names, parameters, or operational details mentioned in the original works are **not** reproduced in our demos. |
| **Human-in-the-Loop by Design** | Papers advocating autonomous agent action (e.g., RL policies that act without human gates) are adapted to include explicit human confirmation steps. Agent outputs remain *recommendations*, never *directives*. |
| **Explainability at Every Level** | Techniques adopted from these references preserve inspectable reasoning traces. Opaque scoring functions or black-box decision mechanisms described in the literature are re-implemented with published rubrics and transparent agent prompts. |
| **No Real Doctrinal Authority** | References to military doctrine (OODA, MDMP, F2T2EA, Boyd, Mahan, Corbett, Vego) are treated as publicly available conceptual frameworks for educational purposes — never as authoritative operational guidance. |
| **Scope Limitation** | The research value of each paper is bounded to its contribution to synthetic, educational rapid-prototyping. Findings are not extended to make claims about real-world operational effectiveness. |

> *Readers should note: the presence of a reference does not imply endorsement of all claims within it. Each paper is evaluated critically, and only the architectural patterns, theoretical frameworks, and methodological approaches relevant to responsible, human-centered AI prototyping are adopted.*

---

## 1. `2408_13333v1.pdf`

**Full Title:** Mastering the Digital Art of War: Developing Intelligent Combat Simulation Agents for Wargaming Using Hierarchical Reinforcement Learning

**Author:** Scotty E. Black (Lieutenant Colonel, USMC)

**Source:** Doctoral Dissertation, Naval Postgraduate School, Monterey, CA, June 2024. Distribution Statement A — Approved for public release.

**Calhoun Handle:** https://hdl.handle.net/10945/73072

**Summary:** Proposes a comprehensive hierarchical reinforcement learning (HRL) framework for developing intelligent agents in the Atlatl turn-based combat simulation. The dissertation introduces four interlocking contributions: (1) localized observation abstractions using piecewise linear spatial decay that allow RL agents to scale to larger gameboards; (2) a multi-model framework that combines scripted and RL-trained behavior models, using neural-network score prediction to select the best model at each action-selection step — achieving a 62.6% improvement over the top-performing single model; (3) a hybrid AI framework that pairs RL for high-level decisions with scripted agents for lower-level tasks; and (4) the overarching HRL architecture that decomposes decisions across Commander, Manager, and Operator levels with different observation abstractions at each echelon.

**Relevance to this project:** Direct inspiration for Demo 3 (Hierarchical Commander–Manager–Operator Micro-Wargame). The Multi-Model Selector Agent in the demo mirrors Black's score-prediction-based model selection. The observation abstraction hierarchy (coarse → mid → local) maps to the agent architecture where each echelon sees the battlespace at a different resolution. This dissertation is the bridge between the RL-based and LLM-based wargaming research communities that the abstract's presentation explicitly seeks to span.

**Responsible AI note:** Black's RL agents act autonomously within the Atlatl simulation. In our adaptation, human-in-the-loop gates are inserted at each echelon boundary — the Commander agent's decisions require human approval before propagating to Manager and Operator levels. The multi-model selector's scoring rubric is made fully transparent (published in notebook markdown) rather than embedded in opaque neural-network weights.

---

## 2. `2402_06694v1.pdf`

**Full Title:** Developing Intelligent Agents for Combat Simulations Using Hierarchical Reinforcement Learning

**Authors:** Scotty E. Black, Christian J. Darken, Imre Balogh

**Source:** 2023 Interservice/Industry Training, Simulation, and Education Conference (I/ITSEC), Paper No. 23302.

**Summary:** Conference-length precursor to the full dissertation above. Presents the HRL framework at an earlier stage of development, with detailed figures of the Multi-Model Framework (Figure 5) and the three-level Policy Hierarchy. Reports the 62.6% multi-model improvement result and introduces the concept of per-phase score prediction. Outlines the planned integration of RL-based score prediction models for the model-selection mechanism.

**Relevance to this project:** Provides the concise, citable version of the HRL and multi-model concepts for use in a conference presentation or poster. The I/ITSEC audience overlap with the Navy wargaming community makes this the most directly peer-relevant citation. The figures (HRL Framework, Multi-Model Framework) are candidates for inclusion on a poster.

**Responsible AI note:** Same HITL and explainability adaptations as Reference 1. The conference-length format distills claims; we apply the same critical evaluation standard and do not overextend results beyond the reported experimental conditions.

---

## 3. `Large_Language_Models_in_Wargaming_Methodology_Application_and_Robustness.pdf`

**Full Title:** Large Language Models in Wargaming: Methodology, Application, and Robustness

**Authors:** Yuwei Chen, Shiyong Chu

**Source:** 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), pp. 2894–2900.

**DOI:** 10.1109/CVPRW63382.2024.00295

**Summary:** First published work to integrate LLMs into the OODA loop for wargaming decision support. Uses GPT-4 with the commercial wargame "Command Modern Operations" (CMO). The Observe/Orient phases feed battlefield data to the LLM as text; the Decide phase produces strategic recommendations; the Act phase delivers those to the player. Experiments test robustness against adversarial prompts (typos, unit conversions, misleading data) and find GPT-4 resilient to all tested perturbations, though the authors caution this may not generalize to all LLMs.

**Relevance to this project:** Provides the OODA-loop-to-LLM mapping that Demo 1 (Living Scenario Brief) directly extends into a multi-agent architecture. The robustness findings inform the design of the ISR/Intel Fusion Agent (which injects contradictory information to test system resilience). The paper's limitation — single-agent, single-LLM, no multi-agent orchestration — is exactly the gap the demo suite fills using AutoGen.

**Responsible AI note:** Chen & Chu test robustness against adversarial prompts but caution their findings may not generalize. We adopt this epistemic humility: our demos do not claim LLM robustness in operational settings. The paper's use of a commercial wargame (CMO) with real-world-adjacent scenario design is adapted into fully synthetic environments with no real operational data. All explainability requirements (transparent OODA-phase reasoning traces) are enforced where the original single-agent design left them implicit.

---

## 4. `MPSAS19214P.pdf`

**Full Title:** Leveraging Large Language Models for Enhanced Wargaming in Multi-Domain Operations

**Authors:** Captain Max Meltschack, First Lieutenant Dominic Weller

**Source:** NATO Science and Technology Organization, STO-MP-SAS-192, Paper 14P, Office for Defence Planning — German Armed Forces, Munich.

**Summary:** Presents a card-based multi-domain wargame where LLMs serve as both Red player and Blue advisor. The game tracks five quantified dimensions per action: Impact Points, Escalation Points, Communication Score, Political Will, and Resource Points. Players select from Military, Cyber/Hybrid, and Political/Economic action cards each turn. LLMs (GPT-3.5 Turbo, Mistral 7B) generate new cards, play as the Red adversary with transparent reasoning, and provide action recommendations to Blue with point-cost tradeoffs. The game includes escalation tracking (1–10 scale), morale scoring, and news-update generation. Compares LLM outputs across models.

**Relevance to this project:** Direct inspiration for Demo 2 (Gray-Zone Escalation Manager). The five scoring dimensions, card-based action menus, escalation ladder, and LLM-as-Red-player design are adopted and adapted into the AutoGen agent architecture. The comparison between GPT-3.5 and Mistral outputs informs the project's position that the framework should be model-agnostic and portable across LLM providers.

**Responsible AI note:** Meltschack & Weller's escalation tracking (1–10 scale) directly supports explainability — every turn's escalation consequence is numerically visible. We preserve and extend this transparency. The LLM-as-Red-player with "transparent reasoning" aligns with our requirement that adversary-role agents explain their logic. Multi-domain action cards referencing real military capabilities are abstracted into fictional equivalents in our adaptation. The Legal/ROE agent in Demo 2 (absent in the original) is our addition to ensure ethical constraint checking.

---

## 5. `master_Vasankari_Lauri_2024.pdf`

**Full Title:** Multi-Agent Reinforcement Learning for Decision Support in Littoral Naval Warfare

**Author:** Lauri Vasankari

**Source:** Master's Thesis, Aalto University (in cooperation with NPS), 2024.

**Summary:** Demonstrates the use of multi-agent reinforcement learning (MARL) as a tactical decision-making support tool for a Finnish Navy surface warfare task group in the Baltic Sea. Formulates littoral combat as a partially observable stochastic game (POSG) and trains agents using DDQN and MAPPO. The environment models radar detection, EMCON (emission control), cross-fix targeting, and surface-to-surface missile engagements with historical probability data from Schulte (1994). Key contribution: RL-generated COAs are intended to oppose planner and decision-maker bias by producing alternatives "without the subjective, cultural mindset" — explicitly citing Boyd's OODA theory on how orientation is shaped by cultural tradition and prior experience. The thesis maps its work to MDMP steps (COA development, analysis, and comparison) and the F2T2EA kill chain (Find, Fix, Track, Target, Engage, Assess), citing Johnson et al. (2023) from the *Naval Engineers Journal*. Also references Mahan, Corbett, and Vego on strategic and littoral naval warfare principles.

**Relevance to this project:** Strongest theoretical justification for Demo 4 (Counterfactual Bias Testing). Vasankari's argument that AI should oppose planner bias is the intellectual foundation for the Bias/Feedback Auditor Agent. The F2T2EA kill chain mapping is adopted for the poster framework discussion. The MDMP integration validates the demo suite's claim that LLM-based agents can slot into existing military planning processes. The littoral warfare environment design (grid-based, EMCON, missile engagements) informs the tactical layer of Demo 3 (Hierarchical Micro-Wargame).

**Responsible AI note:** Vasankari's thesis makes the strongest responsible AI argument in the collection: that AI-generated COAs should *oppose* human cognitive biases rather than reinforce them. This directly motivates our Bias Auditor Agent, which names specific biases (anchoring, recency, escalation commitment, mirror-imaging, availability heuristic) using accepted terminology. References to Boyd, Mahan, Corbett, and Vego are treated as publicly available conceptual frameworks — not as authoritative doctrinal sources. The thesis's real-world Finnish Navy context is replaced entirely with synthetic scenarios in our adaptation.

---

## 6. `applsci0901089.pdf`

**Full Title:** A Multi-Agent Based Intelligent Training System for Unmanned Surface Vehicles

**Authors:** Wei Han, Bing Zhang, Qianyi Wang, Jun Luo, Weizhi Ran, Yang Xu

**Source:** *Applied Sciences*, 2019, 9(6), 1089. MDPI. DOI: 10.3390/app9061089

**Summary:** Presents a multi-agent training system for teams of unmanned surface vehicles (USVs) in an island-conquering maritime scenario. Uses genetic fuzzy trees (GFTs) to learn cooperative decision rules in a partially observable stochastic game (POSG) where no historical behavioral data is available. Agents are decomposed into task-level decision trees (Task → Intercept/Conquer → Assist/Operation/Track) with leaf-node actions (retreat, left, right, stop, straight, assist, units, closest). Introduces probabilistic goal-recognition functions (PGFs) to estimate opponent intent from observed behavior, enabling agents to adapt to non-stationary adversaries.

**Relevance to this project:** Provides the foundational multi-agent architecture concepts (decomposed decision trees, belief-based opponent modeling, team coordination without historical data) that inform how the AutoGen agents in the demo suite should structure their reasoning. The fuzzy-logic approach to opponent intent estimation is an analog to what the Red Team Agent in Demo 2 does with natural language: infer adversary objectives from observed actions and adapt accordingly. The island-conquering scenario's reward structure (balancing conquest vs. combat vs. survival) is echoed in the multi-dimensional scoring of Demo 2's Gray-Zone Escalation Manager.

**Responsible AI note:** Han et al.'s multi-agent USV system operates autonomously (genetic fuzzy trees selecting actions without human input). In our adaptation, analogous decision trees are replaced by LLM agents with human-in-the-loop checkpoints. The opponent-modeling mechanism (probabilistic goal-recognition functions) is made explainable through natural-language reasoning traces rather than opaque probability distributions. Real USV platforms and weapons parameters from the original paper are not reproduced; all tactical elements use synthetic abstractions.

---

## How These References Relate to Each Other

```
                    ┌─────────────────────────────────┐
                    │  This Project: AutoGen + Python  │
                    │  LLM Multi-Agent Demo Suite      │
                    └──────────────┬──────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                     │
     RL / Simulation          LLM / Wargaming       Naval Domain
     Foundations              Applications          Knowledge
              │                    │                     │
   ┌──────────┴──────────┐   ┌────┴─────┐        ┌─────┴──────┐
   │ Black (NPS 2024)    │   │ Chen &   │        │ Vasankari  │
   │ - HRL framework     │   │ Chu 2024 │        │ (Aalto/NPS)│
   │ - Multi-model       │   │ - OODA + │        │ - MARL for │
   │ - Observation       │   │   LLM    │        │   littoral │
   │   abstraction       │   │ - CMO    │        │ - F2T2EA   │
   │ - Atlatl sim        │   │   game   │        │ - MDMP     │
   │                     │   │          │        │ - Bias     │
   │ Black et al.        │   │ Melt-    │        │   opposition│
   │ (I/ITSEC 2023)      │   │ schack & │        │            │
   │ - Conference paper  │   │ Weller   │        │ Han et al. │
   │   of above          │   │ (NATO)   │        │ (ApplSci)  │
   │                     │   │ - Card   │        │ - USV multi│
   └─────────────────────┘   │   wargame│        │   agent    │
                             │ - Multi- │        │ - Fuzzy    │
                             │   domain │        │   decision │
                             │ - Scoring│        │   trees    │
                             └──────────┘        └────────────┘
```

The RL/simulation papers (Black) provide the hierarchical architecture and multi-model selection mechanism. The LLM/wargaming papers (Chen & Chu; Meltschack & Weller) provide the methodology for integrating LLMs into decision loops and the precedent for LLM-driven adversary play. The naval domain papers (Vasankari; Han et al.) provide the tactical knowledge base, the bias-opposition argument, and the multi-agent coordination patterns. This project synthesizes all three threads into a single AutoGen-based rapid prototyping framework.

### Responsible AI Thread Across the Literature

A unifying responsible AI reading emerges across all six references:

- **From autonomy to advisory:** The RL papers (Black, Han) build fully autonomous agents. The LLM papers (Chen & Chu, Meltschack & Weller) begin introducing human players. Vasankari explicitly argues for AI as bias-opposition rather than decision-maker. Our project completes this arc: every agent is advisory, every consequential action requires human approval.
- **From opaque to explainable:** Genetic fuzzy trees (Han) and neural score predictors (Black) are opaque by nature. Card-game scoring (Meltschack & Weller) introduces dimensional transparency. Our project mandates full explainability — every agent chain terminates in a human-readable reasoning trace.
- **From real-adjacent to fully synthetic:** Several references use real-world-adjacent scenarios (CMO in Chen & Chu, Finnish Navy in Vasankari, real USV platforms in Han). Our project enforces a strict synthetic-only boundary, adapting architectural insights while discarding operational specifics.
- **From implicit to explicit bias awareness:** Only Vasankari explicitly addresses cognitive bias. Our project elevates bias detection to a first-class architectural concern (Demo 4's Bias Auditor Agent), informed by Vasankari's argument but extended with structured bias taxonomies and appeal mechanisms.

---

## Citation Format (for use in presentations)

```
[1] S. E. Black, "Mastering the Digital Art of War: Developing Intelligent
    Combat Simulation Agents for Wargaming Using Hierarchical Reinforcement
    Learning," Ph.D. dissertation, Naval Postgraduate School, Monterey, CA,
    June 2024.

[2] S. E. Black, C. J. Darken, and I. Balogh, "Developing Intelligent Agents
    for Combat Simulations Using Hierarchical Reinforcement Learning," in
    Proc. I/ITSEC 2023, Paper No. 23302, 2023.

[3] Y. Chen and S. Chu, "Large Language Models in Wargaming: Methodology,
    Application, and Robustness," in Proc. IEEE/CVF CVPRW 2024,
    pp. 2894–2900, 2024.

[4] M. Meltschack and D. Weller, "Leveraging Large Language Models for
    Enhanced Wargaming in Multi-Domain Operations," NATO STO-MP-SAS-192,
    Paper 14P, 2024.

[5] L. Vasankari, "Multi-Agent Reinforcement Learning for Decision Support
    in Littoral Naval Warfare," M.S. thesis, Aalto University, 2024.

[6] W. Han, B. Zhang, Q. Wang, J. Luo, W. Ran, and Y. Xu, "A Multi-Agent
    Based Intelligent Training System for Unmanned Surface Vehicles,"
    Applied Sciences, vol. 9, no. 6, p. 1089, 2019.
```
