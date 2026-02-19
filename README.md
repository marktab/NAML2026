# Rapid Prototyping of Multi-Agent AI Decision Support in Synthetic Naval Scenarios

## Poster Companion — NAML 2026

*This repository accompanies the poster presentation at the Naval Applications of Machine Learning (NAML) conference. It contains five runnable Jupyter notebook demos that illustrate how multi-agent AI architectures can support human decision-making in synthetic naval scenarios. Everything here — code, data, and scenarios — is fully synthetic and open for exploration.*

> **Responsible AI & Scope Statement:** This research explores human-AI collaboration and explainable decision-support in fully synthetic, abstract environments. All scenarios, agents, and data are artificially generated. No real-world operational data, contingency plans, systems, or intelligence are used or represented. The prototype is intended exclusively for research, educational, and experimental purposes and does not constitute an operational model, validated planning tool, or source of decision authority.

---

## The Big Idea in One Paragraph

AI is not replacing commanders — it is helping them **understand evolving situations**, **reason across complexity**, **learn from experience**, and **make better-informed decisions**. This demo suite uses multiple specialized AI agents that collaborate on a shared problem, each contributing a distinct capability (intelligence fusion, legal review, adversary modeling, bias detection, explainability). Presentation order mirrors the operational cycle a warfighter experiences: understand the situation → engage under ambiguity → scale decisions across echelons → stress-test reasoning → extract institutional knowledge. Each demo maps to one or more phases of the [OODA loop](https://en.wikipedia.org/wiki/OODA_loop), and together they tell a single coherent story.

---

## What Is Multi-Agent AI?

Traditional AI assistants use a **single model** to handle an entire task. Multi-agent AI takes a different approach: it decomposes a complex problem across **multiple specialized agents**, each with its own role, instructions, and perspective. The agents communicate through structured messages, debate conclusions, and produce a coordinated output — much like a well-run staff process.

**Why does this matter for military decision support?**

| Single-Agent Approach | Multi-Agent Approach |
|---|---|
| One model does everything — analysis, planning, critique, explanation | Separate agents for analysis, planning, red-teaming, legal review, explanation |
| Hard to audit which "part" of the model produced a conclusion | Each agent's contribution is individually inspectable |
| Difficult to enforce constraints (e.g., ROE compliance) | A dedicated Legal/ROE agent enforces constraints at every turn |
| No built-in adversarial challenge | A Red Team agent actively challenges Blue's reasoning |
| Explanation is an afterthought | A dedicated Explainability Agent traces every decision chain |

In this project, agents are orchestrated using **Microsoft AutoGen**, an open-source framework for building multi-agent applications.

> **Learn more:** [What is AutoGen?](https://microsoft.github.io/autogen/) · [AutoGen on GitHub](https://github.com/microsoft/autogen) · [Multi-agent design patterns (Microsoft Research)](https://www.microsoft.com/en-us/research/blog/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/)

---

## Azure Technology Primer

If you are new to Azure, this section explains the four Azure services this project uses and why each one matters. No Azure experience is required to read the demos, but understanding the stack will help you see how a prototype like this moves from a laptop to a secure, scalable deployment.

### Azure AI Foundry — The LLM Endpoint

**What it is:** [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/what-is-azure-ai-foundry) (formerly Azure AI Studio) is Microsoft's platform for deploying and managing AI models. It provides API endpoints for large language models (LLMs) like GPT-4o — the same models that power these demos. You deploy a model, get an HTTPS endpoint, and call it from your code. Azure AI Foundry also supports the [Azure AI model inference API](https://learn.microsoft.com/azure/ai-foundry/model-inference/overview), a unified API that works across model providers.

**How this project uses it:** Every AutoGen agent in the demos sends its prompts to an Azure AI Foundry endpoint. The `common/config.py` module retrieves the endpoint URL and API key from Azure Key Vault (see below), then passes them to AutoGen's model client. Swapping models (e.g., GPT-4o → a smaller model for edge deployment) requires only a configuration change — no code changes.

> **Learn more:** [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/) · [Quickstart: Deploy and chat with a model](https://learn.microsoft.com/azure/ai-foundry/quickstarts/get-started-playground) · [Azure OpenAI Service overview](https://learn.microsoft.com/azure/ai-services/openai/overview) · [What models are available?](https://learn.microsoft.com/azure/ai-services/openai/concepts/models)

### Azure Key Vault — Secure Credential Management

**What it is:** [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/overview) is a cloud service for securely storing and accessing secrets — API keys, connection strings, certificates, and encryption keys. Secrets are stored in FIPS 140-2 validated, hardware-backed security modules. Access is controlled by fine-grained policies (who can read which secret, and when), and every access is audit-logged.

**Why it matters (especially for DoD):** Hard-coding API keys in source code is a serious security risk — Git history is permanent, and a leaked key can be harvested by automated scanners. Compliance frameworks like NIST 800-53, FedRAMP, and DoD IL4/IL5 require centralized key management with auditable access. Key Vault satisfies all of these requirements and supports network isolation via private endpoints for secure enclaves.

**How this project uses it:** The `common/config.py` module reads the AI Foundry endpoint URL and API key from Key Vault at runtime. No credentials are ever stored in code, notebooks, or configuration files checked into version control.

> **Learn more:** [Azure Key Vault overview](https://learn.microsoft.com/azure/key-vault/general/overview) · [Quickstart: Set and retrieve a secret](https://learn.microsoft.com/azure/key-vault/secrets/quick-create-portal) · [Best practices for using Key Vault](https://learn.microsoft.com/azure/key-vault/general/best-practices)

### Azure Identity & DefaultAzureCredential — Zero-Secret Authentication

**What it is:** The [Azure Identity library](https://learn.microsoft.com/python/api/overview/azure/identity-readme) provides a `DefaultAzureCredential` class that automatically authenticates your code to Azure services. It tries a chain of credential sources in order — Managed Identity (when running in Azure), Azure CLI login (for local development), environment variables, and others — so your code works across environments without modification.

**How this project uses it:** When the config module connects to Key Vault, it uses `DefaultAzureCredential`. On a developer laptop, this authenticates via `az login`. In an Azure-hosted environment, it uses [Managed Identity](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview) — no credentials touch the codebase in either case.

> **Learn more:** [DefaultAzureCredential overview](https://learn.microsoft.com/python/api/overview/azure/identity-readme#defaultazurecredential) · [Managed identities for Azure resources](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview)

### Azure Government Cloud — IL4 to IL6+ Portability

**What it is:** [Azure Government](https://learn.microsoft.com/azure/azure-government/documentation-government-welcome) is a physically isolated instance of Azure designed for U.S. government workloads. It meets FedRAMP High, DoD IL4, IL5, and IL6 compliance requirements and is operated by screened U.S. persons.

**How this project uses it:** The demos are designed to be **portable across impact levels**. They run on a standard laptop with a commercial Azure endpoint during development, but can point at an Azure Government endpoint (e.g., `usgovcloudapi.net`) with only a configuration change. The Key Vault URL in `common/config.py` already defaults to an Azure Government endpoint. No code changes are required to move between commercial and government clouds.

> **Learn more:** [Azure Government documentation](https://learn.microsoft.com/azure/azure-government/documentation-government-welcome) · [Azure Government compliance](https://learn.microsoft.com/azure/compliance/offerings/offering-dod-il4) · [Compare Azure Government and global Azure](https://learn.microsoft.com/azure/azure-government/compare-azure-government-global-azure)

### How the Pieces Fit Together

```
┌─────────────────────────────────────────────────────────────┐
│  Jupyter Notebook (Demo 1–5)                                │
│    └── AutoGen agents (group chat / sequential chat)        │
│          └── Each agent sends prompts to ───────────────┐   │
│                                                         │   │
│  common/config.py                                       │   │
│    ├── DefaultAzureCredential ──► Azure Key Vault       │   │
│    │       (retrieves endpoint URL + API key)           │   │
│    └── InferenceConfig ──────────► Azure AI Foundry ◄───┘   │
│              (LLM endpoint: GPT-4o)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Responsible AI Guiding Principles

The following principles govern every demo, agent, and line of code in this repository. They are not optional add-ons — they are **architectural requirements** that shape design decisions across the entire suite.

### 1. Fully Synthetic Data Only

All scenario content — actors, locations, events, timelines, coordinates, and force compositions — is **entirely fictional and synthetically generated**. No real-world operational data, contingency plans, intelligence products, classified material, or real military unit designations are used or referenced anywhere in this repository. The demos have **zero external data dependencies** by design. World-state JSON includes explicit synthetic-data markers and disclaimer fields.

### 2. Human-in-the-Loop by Design

AI agents **never** take autonomous consequential actions. All agent outputs are framed as **recommendations and analysis** — never orders, directives, or commands. Every interactive decision point includes a human confirmation gate before the system proceeds. Consequential actions (e.g., intercept, engagement) require explicit human approval. Demos 2, 4, and 5 feature interactive human turns; Demo 4 is specifically designed for audience participation where the system surfaces the participant's own reasoning patterns in real time. **All decisions remain with the human operator at all times.**

### 3. Explainability as a Through-Line

Every demo includes a dedicated **Explainability Agent** that produces transparent, inspectable reasoning traces. Every agent chain terminates in an explanation of *why* the system reached its conclusion. Scoring rubrics and decision rationale are published and visible in the notebooks — never hidden in opaque function calls. Bias detection outputs name specific cognitive biases by their accepted terms (anchoring, recency bias, escalation commitment, mirror-imaging, availability heuristic) and produce structured appeal briefs. This directly addresses the central concern in the AI decision-support literature: trust and transparency.

### 4. No Real Doctrinal Authority

Doctrinal references are **inspired by publicly available concepts** and abstracted from open-source military decision-making frameworks for educational purposes only. This repository **does not** represent authoritative U.S. Navy doctrine, operational procedures, or rules of engagement. It does not constitute an operational model, validated planning tool, or source of decision authority.

### 5. Scope-Bounded Research Purpose

This prototype is intended **exclusively for research, educational, and experimental purposes**. Every notebook reinforces this scope boundary. The system is a research instrument for exploring how multi-agent AI architectures can support human decision-making — not a replacement for professional military judgment, trained staff processes, or validated operational tools.

### Responsible AI Checklist — Every Change, Every Contribution

| Check | Question |
|-------|----------|
| **Synthetic?** | Does all scenario content remain artificial and clearly labeled? |
| **HITL preserved?** | Is there a human decision gate before any consequential action? |
| **Explainable?** | Can a reviewer trace how and why the system reached its output? |
| **Scope-bounded?** | Does the change stay within the research/educational purpose? |
| **Secrets safe?** | Are credentials retrieved from Key Vault, never hardcoded? |
| **Cross-demo compatible?** | Does `smoke_run.py` still pass? |
| **Portable?** | Would this run on any Python + LLM endpoint environment? |

---

## Demo Overview

| # | Demo | OODA Phase | Warfighter Activity | Details |
|---|------|------------|---------------------|---------|
| 1 | **Living Scenario Brief** | Observe / Orient | Understand the situation | [README](demos/demo1_living_brief/README.md) |
| 2 | **Gray-Zone Escalation Analysis Sandbox** | Orient / Decide / Act | Engage under ambiguity | [README](demos/demo2_grayzone_rbw/README.md) |
| 3 | **Hierarchical Decision-Flow Simulation** | Decide / Act (across echelons) | Scale decisions across echelons | [README](demos/demo3_hierarchical_c2/README.md) |
| 4 | **Counterfactual COA Analysis** | Orient / Decide boundary | Stress-test reasoning | [README](demos/demo4_counterfactual_coa/README.md) |
| 5 | **After-Action Replay & Doctrinal Clinic** | Loop closure → future O/O | Extract institutional knowledge | [README](demos/demo5_aar_doctrinal_clinic/README.md) |

### Why This Order Works

1. **Demo 1** establishes shared situational understanding — the foundation everything else depends on
2. **Demo 2** shows decision-making under ambiguity and competing equities — the hardest thing commanders do
3. **Demo 3** scales those decisions across a realistic command hierarchy — showing the framework handles complexity
4. **Demo 4** stress-tests the reasoning that went into those decisions — the most intellectually novel contribution
5. **Demo 5** extracts institutional learning from everything that just happened — the deliverable that justifies the investment

> **If time is constrained:** Demos 1, 2, and 5 can be run as a minimal viable chain (understand → play → learn). Demos 3 and 4 can be presented as slides with pre-recorded output.

---

### Demo 1 — "Living Scenario Brief": Adaptive Situational Awareness Under Uncertainty

A multi-agent scenario-learning loop that maintains a living world state (structured JSON of events, actors, locations, and uncertainties) and updates it each turn as new simulated intelligence arrives. Each cycle produces a structured SITREP explaining what changed and why — with every assessment accompanied by a one-sentence evidence citation supporting transparent, explainable reasoning. Built around the OODA Observe/Orient phases and connected with established military decision-making frameworks (Chen & Chu, CVPRW 2024), this is the most accessible demo in the suite — every warfighter knows what a SITREP is — and it teaches the audience how multi-agent orchestration works before the scenarios grow more complex. The ISR/Intel Fusion Agent injects realistic noise (confirmations, contradictions, and novel actors) with tunable noise levels to demonstrate graceful degradation under information overload.

**Agents:** Scenario Orchestrator · ISR/Intel Fusion · Assessment · Briefing/Explainer · Human-in-the-Loop (Commander)

### Demo 2 — Maritime Gray-Zone Escalation Analysis Sandbox: Red / Blue / White Cell Play

Simulates a multi-turn gray-zone maritime encounter where Red, Blue, and White cell agents play against each other across turns. Tracks escalation, strategic messaging, legal compliance, and operational objectives using quantified scoring dimensions — Impact, Escalation, Communication, Political, and Resource — inspired by the NATO STO-MP-SAS-192 card-based wargame approach (Meltschack & Weller, German Armed Forces). A Legal/ROE Agent constrains Blue's available actions based on current posture and escalation level, and a Strategic Communications Agent drafts public statements and predicts adversary media response — illustrating the information-warfare dimension underrepresented in the current wargaming AI literature. A dedicated Explainability Agent produces transparent reasoning traces after each turn, identifies potential cognitive biases, and verifies that all outputs remain within the scope of recommendations. Produces a game log that Demo 5 can consume directly for live after-action review.

**Agents:** Blue Planner · Red Team · White Cell/Umpire · Legal/ROE · Strategic Communications · Explainability

### Demo 3 — Hierarchical Decision-Flow Simulation

A compact micro-wargame where decisions decompose across a three-level command hierarchy: Commander sets intent and prioritizes objectives, Managers (Surface and Air Warfare) propose resource allocations and create synchronized sub-plans, and Operators carry out recommended actions on a simple grid. A Multi-Model Selector visibly chooses between scripted heuristics (for routine situations) and LLM reasoning (for higher-level tradeoffs or novel encounters) at each decision step — the selection logic and rationale are visible to the audience. This bridges the RL-based and LLM-based wargaming research communities (Boron et al., NPS 2024; Boron et al., I/ITSEC 2023) and demonstrates that the architecture can swap in different reasoning engines depending on the deployment environment. Consequential actions such as INTERCEPT require explicit human confirmation. A Feedback Aggregator closes the tactical feedback loop, and an Explainability Agent traces the causal chain from Commander intent through Manager plans to Operator outcomes.

**Agents:** Commander · Surface/Air Warfare Managers · Operators · Multi-Model Selector · Feedback Aggregator · Explainability

### Demo 4 — Counterfactual COA Analysis

When a user accepts or rejects a course of action, the system generates "nearby worlds" — scenarios that differ by a single assumption (weather, readiness, adversary intent, ROE constraints, comms reliability, alliance posture) — and tests whether the preference holds. Inconsistent preferences across near-identical worlds are flagged with named cognitive biases (anchoring, recency bias, escalation commitment, mirror-imaging, availability heuristic) and a structured "appeal brief" explaining what assumption changed, what stayed constant, and why the recommendation does or doesn't remain valid. The scoring rubric is published in the notebook for full transparency. This is the most intellectually novel demo in the suite, directly embodying the abstract's emphasis on counterfactual reasoning and bias exposure. The strongest audience engagement moment: the presenter invites an audience member to make choices and then watches the system surface their own reasoning patterns.

**Agents:** COA Generator · Counterfactual Perturbation · Bias/Feedback Auditor · Explainability · Adjudication · Planner-in-the-Loop

### Demo 5 — After-Action Replay and Doctrinal Clinic: Learning from the Game

Given a completed game log from any preceding demo, agents reconstruct the decision timeline, identify the 3–5 most consequential pivotal turning points, evaluate each decision against an abstracted doctrinal knowledge base inspired by publicly available naval warfare concepts, and produce a structured AAR with "Lessons Observed" in a familiar military format: Observation, Discussion, Recommendation, and Implication for Training. The user drives interactive interrogation — selecting decision points, asking "what if?", and watching counterfactual branches generated on the spot using Demo 4's reusable engine. The system adapts its analysis to the user's focus rather than dumping a fixed report, modeling the interactive facilitation style of a skilled AAR leader. For maximum conference impact, the presenter runs Demo 2 live, then pipes that game log directly into Demo 5 for immediate analysis.

**Agents:** Replay Narrator · Doctrinal Critic · Counterfactual Branch · Lessons Learned Compiler · Explainability · Interactive Facilitator (Human-in-the-Loop)

---

## Cross-Cutting Design Principles

- **Consistent AutoGen Pattern** — All demos use [AutoGen 0.7](https://microsoft.github.io/autogen/) group-chat or sequential-chat orchestration with `AssistantAgent` and explicit `system_message` prompts. A common world-state JSON structure is shared across agents, making these a coherent framework rather than isolated prototypes.

- **Explainability as a Through-Line** — Every demo includes a dedicated Explainability Agent whose role is to explain *why* the system reached its conclusion, addressing the central concern in the literature: trust and transparency in AI-assisted decision-making.

- **Human-in-the-Loop by Design** — Demos 2, 4, and 5 feature interactive human turns. Demo 4 is specifically designed for audience participation where the system surfaces the participant's own reasoning biases in real time. All agent outputs are recommendations and analysis — never orders or directives.

- **Cross-Demo Technical Connections** — The counterfactual engine from Demo 4 is reused in Demo 5. The world-state JSON from Demo 1 is the same structure used in Demos 2 and 3. Demo 2's game log is the direct input to Demo 5. The framework is composable.

- **Portability from IL4 to IL6+** — All demos run in standard Python notebooks with no external data dependencies and no infrastructure beyond an LLM API endpoint. For Azure-hosted environments, AutoGen agents can point at [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/) endpoints with no code changes beyond configuration. All credential management goes through [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/overview) via `common/config.py`. See the [Azure Technology Primer](#azure-technology-primer) above for details.

---

## Repository Structure

```
├── README.md                          ← You are here
├── requirements.txt                   ← Python dependencies
├── naml2026.yml                       ← Conda environment definition
├── common/                            ← Shared utilities across all demos
│   ├── __init__.py
│   ├── config.py                      ← Azure AI Foundry / Key Vault config
│   ├── logging.py                     ← Structured logging for agent traces
│   └── ui.py                          ← Display helpers for notebooks
├── demos/
│   ├── demo1_living_brief/            ← Observe / Orient
│   ├── demo2_grayzone_rbw/            ← Orient / Decide / Act
│   ├── demo3_hierarchical_c2/         ← Decide / Act (across echelons)
│   ├── demo4_counterfactual_coa/      ← Orient / Decide boundary
│   └── demo5_aar_doctrinal_clinic/    ← Loop closure
├── references/                        ← Supporting literature and resources
└── scripts/
    └── smoke_run.py                   ← Quick validation across all demos
```

---

## Getting Started

### Prerequisites

- **Python 3.10+** and [Jupyter](https://jupyter.org/)
- An **Azure AI Foundry** (or Azure OpenAI) endpoint with a deployed model (GPT-4o by default)
- An **Azure Key Vault** containing two secrets: `AzureOpenAIProjectEndpoint` and `AzureOpenAIProjectKey`
- Azure CLI (`az login`) for local authentication, or a configured [Managed Identity](https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/overview) in Azure

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Credentials

Set the Key Vault URL as an environment variable (or rely on the default in `common/config.py`):

```bash
export KEY_VAULT_URL="https://<your-vault-name>.vault.azure.net/"
```

For local development, authenticate with:

```bash
az login
```

The `DefaultAzureCredential` in `common/config.py` handles the rest — it retrieves your endpoint and API key from Key Vault automatically. No credentials are stored in code.

### Run the Demos

Each demo is a self-contained Jupyter notebook in its `demos/` subdirectory. Open any notebook and run cells sequentially. See the individual demo READMEs for scenario-specific setup and usage notes.

To validate that all demos load and run correctly:

```bash
python scripts/smoke_run.py
```

---

## References

This repository is grounded in six peer-reviewed sources:

1. Black, S. E. (2024). *Mastering the digital art of war: Intelligent combat simulation agents for wargaming using hierarchical RL.* Naval Postgraduate School.
2. Black, S. E. & Darken, C. (2023). *Scaling intelligent agents in combat simulations for wargaming.* Naval Postgraduate School.
3. Chen, Y. & Chu, S. (2024). *Large language models in wargaming: Methodology, application, and robustness.* IEEE/CVF CVPRW.
4. Han, W. et al. (2019). *A multi-agent based intelligent training system for unmanned surface vehicles.* Applied Sciences, 9(6), 1089.
5. Vasankari, L. (2023). *Multi-agent reinforcement learning for littoral naval warfare.* Aalto University.
6. Weller, D. et al. (2024). *Leveraging LLMs for enhanced wargaming in multi-domain operations.* NATO STO-MP-SAS-192.

---

## Key Links

| Resource | URL |
|----------|-----|
| AutoGen Framework | https://microsoft.github.io/autogen/ |
| Azure AI Foundry | https://learn.microsoft.com/azure/ai-foundry/ |
| Azure OpenAI Service | https://learn.microsoft.com/azure/ai-services/openai/overview |
| Azure Key Vault | https://learn.microsoft.com/azure/key-vault/general/overview |
| Azure Identity (Python) | https://learn.microsoft.com/python/api/overview/azure/identity-readme |
| Azure Government | https://learn.microsoft.com/azure/azure-government/ |
| Responsible AI (Microsoft) | https://www.microsoft.com/ai/responsible-ai |

