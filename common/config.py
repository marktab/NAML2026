"""
Shared configuration primitives for the NAML 2026 demo notebooks.

Responsible AI Notice
---------------------
This module enforces the project's Responsible AI constraints at the
configuration level.  Every demo inherits synthetic-data markers, HITL
requirements, explainability flags, and scope-boundary language from the
constants defined here.  See the project's ``responsible-ai-prompt.md``
for the full policy.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


# ═══════════════════════════════════════════════════════════════
# RESPONSIBLE AI CONSTANTS
# ═══════════════════════════════════════════════════════════════

SYNTHETIC_DATA_MARKER: bool = True
"""Every world-state JSON must include ``"synthetic": true``."""

SYNTHETIC_DATA_DISCLAIMER: str = (
    "All data is artificially generated for research and educational "
    "purposes only."
)
"""Required ``disclaimer`` field value in all world-state JSON."""

SCOPE_STATEMENT: str = (
    "This research explores human-AI collaboration and explainable "
    "decision-support in fully synthetic, abstract environments. All "
    "scenarios, agents, and data are artificially generated. No real-world "
    "operational data, contingency plans, systems, or intelligence are used "
    "or represented. The prototype is intended exclusively for research, "
    "educational, and experimental purposes and does not constitute an "
    "operational model, validated planning tool, or source of decision "
    "authority."
)
"""Must appear in every notebook's Responsible AI & Scope Statement cell."""

HITL_SYSTEM_PROMPT: str = (
    "All decisions remain with the human operator. You provide analysis "
    "and options, not directives."
)
"""Fragment to inject into every agent's system_message."""

DOCTRINAL_DISCLAIMER: str = (
    "Inspired by publicly available doctrinal concepts. This system does "
    "not represent authoritative doctrine, operational procedures, or "
    "rules of engagement."
)
"""Required whenever doctrinal references appear (especially Demo 5)."""

COGNITIVE_BIASES: Tuple[str, ...] = (
    "anchoring",
    "recency bias",
    "escalation commitment",
    "mirror-imaging",
    "availability heuristic",
)
"""Named biases the Bias Auditor (Demo 4) must detect and report."""

RECOMMENDATION_VERBS: Tuple[str, ...] = (
    "recommends",
    "assesses",
    "suggests",
    "evaluates",
    "proposes",
)
"""Acceptable agent-output framing verbs (never 'directs', 'orders', 'commands')."""

FORBIDDEN_ACTION_VERBS: Tuple[str, ...] = (
    "directs",
    "orders",
    "commands",
    "authorizes",
    "executes",
)
"""Verbs that must NOT appear as agent-output framing language."""


# ═══════════════════════════════════════════════════════════════
# KEY VAULT + LLM SETTINGS
# ═══════════════════════════════════════════════════════════════
#
# Why Azure Key Vault?
# --------------------
# Credentials (API keys, connection strings, tokens) must NEVER be
# hard-coded in source files, notebooks, or configuration checked into
# version control.  Embedding secrets in code creates serious risks:
#
#   1. Source-control exposure — Git history is permanent.  A key that
#      is committed even briefly can be harvested by automated scanners
#      or leaked through forks and mirrors.
#   2. Lateral movement — A single leaked credential may grant access
#      to broader cloud resources, AI model endpoints, or data stores.
#   3. Compliance violations — Frameworks such as NIST 800-53 (SC-12,
#      SC-28), FedRAMP, and DoD IL4/IL5 require centralized key
#      management with auditable access policies.  Hard-coded secrets
#      fail every one of these controls.
#   4. Rotation difficulty — Secrets embedded across multiple files
#      cannot be rotated centrally, increasing the blast radius of a
#      compromise and making incident response slower.
#
# Azure Key Vault addresses these risks by storing secrets in a
# FIPS 140-2 validated, hardware-backed service with:
#   • Fine-grained RBAC and access policies (who/what can read which
#     secret, and when).
#   • Full audit logging of every secret access via Azure Monitor.
#   • Automatic secret rotation and expiration policies.
#   • Network isolation — Key Vault can be locked to specific VNets
#     and private endpoints, supporting IL4+ deployment postures.
#
# In this project the ``DefaultAzureCredential`` chain authenticates
# transparently: via Managed Identity in Azure, or via ``az login`` /
# environment variables during local development — so no credential
# material ever touches the codebase.
#
# Getting started:
#   https://learn.microsoft.com/azure/key-vault/general/overview
#
# ─────────────────────────────────────────────────────────────────

ENV_KEY_VAULT_URL = "KEY_VAULT_URL"
DEFAULT_KEY_VAULT_URL = "https://marktabkeys.vault.usgovcloudapi.net/"

# Secret names in Key Vault — these reference the *names* of secrets
# stored in the vault, never the secret values themselves.
KV_SECRET_INFERENCE_ENDPOINT = "AzureOpenAIProjectEndpoint"
KV_SECRET_INFERENCE_KEY = "AzureOpenAIProjectKey"

# Optional: allow env-var override (useful for local dev or emergency).
# Even when using this fallback, values should come from a secure
# source (e.g. a .env file excluded via .gitignore), never literals.
ENV_AZURE_INFERENCE_ENDPOINT = "AZURE_INFERENCE_ENDPOINT"
ENV_AZURE_INFERENCE_CREDENTIAL = "AZURE_INFERENCE_CREDENTIAL"

DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.3
DEFAULT_TIMEOUT_S = 120
DEFAULT_RETRY_LIMIT = 2


@dataclass(frozen=True)
class InferenceConfig:
    endpoint: str
    api_key: str
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    timeout_s: int = DEFAULT_TIMEOUT_S
    retry_limit: int = DEFAULT_RETRY_LIMIT


def _get_secret(vault_url: str, secret_name: str) -> str:
    """
    Read one secret from Key Vault using DefaultAzureCredential.
    Works in Azure via Managed Identity and locally via az login / env vars.
    """
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    return client.get_secret(secret_name).value  # type: ignore[return-value]


def load_inference_config() -> InferenceConfig:
    vault_url = os.getenv(ENV_KEY_VAULT_URL) or DEFAULT_KEY_VAULT_URL

    # Key Vault path
    if vault_url:
        endpoint = _get_secret(vault_url, KV_SECRET_INFERENCE_ENDPOINT)
        api_key = _get_secret(vault_url, KV_SECRET_INFERENCE_KEY)

        # IMPORTANT: match what your working notebook patch does
        os.environ[ENV_AZURE_INFERENCE_ENDPOINT] = endpoint
        os.environ[ENV_AZURE_INFERENCE_CREDENTIAL] = api_key

        return InferenceConfig(endpoint=endpoint, api_key=api_key)

    # Fallback (no vault url configured)
    endpoint = os.getenv(ENV_AZURE_INFERENCE_ENDPOINT)
    api_key = os.getenv(ENV_AZURE_INFERENCE_CREDENTIAL)
    if not endpoint or not api_key:
        raise RuntimeError(
            "Missing inference configuration. Set KEY_VAULT_URL (recommended) "
            "or set AZURE_INFERENCE_ENDPOINT and AZURE_INFERENCE_CREDENTIAL."
        )
    return InferenceConfig(endpoint=endpoint, api_key=api_key)

# Auto-initialize env vars for notebooks that expect AZURE_INFERENCE_* to exist.
# This keeps legacy notebooks working without requiring an explicit call.
try:
    if not os.getenv(ENV_AZURE_INFERENCE_ENDPOINT) or not os.getenv(ENV_AZURE_INFERENCE_CREDENTIAL):
        load_inference_config()
except Exception:
    # Don't block imports if KV auth isn't available; notebook may set env vars another way.
    pass


# ═══════════════════════════════════════════════════════════════
# OODA PHASES — Every demo maps to one or more phases
# ═══════════════════════════════════════════════════════════════

class OODAPhase(str, Enum):
    OBSERVE = "observe"
    ORIENT = "orient"
    DECIDE = "decide"
    ACT = "act"


# ═══════════════════════════════════════════════════════════════
# SCENARIO TYPES (variant conditions applied to any demo)
# ═══════════════════════════════════════════════════════════════

class ScenarioType(str, Enum):
    BASELINE = "baseline"
    HIGH_TEMPO = "high_tempo"
    DEGRADED_COMMS = "degraded_comms"
    ADVERSARY_SURPRISE = "adversary_surprise"


@dataclass(frozen=True)
class ScenarioConfig:
    name: str
    description: str
    parameters: Dict[str, str] = field(default_factory=dict)


SCENARIOS: List[ScenarioConfig] = [
    ScenarioConfig(
        name="Baseline",
        description="Nominal conditions and standard tempo.",
        parameters={"scenario_type": ScenarioType.BASELINE.value},
    ),
    ScenarioConfig(
        name="High Tempo",
        description="Accelerated operations and compressed timelines.",
        parameters={"scenario_type": ScenarioType.HIGH_TEMPO.value},
    ),
    ScenarioConfig(
        name="Degraded Comms",
        description="Intermittent or limited communications.",
        parameters={"scenario_type": ScenarioType.DEGRADED_COMMS.value},
    ),
    ScenarioConfig(
        name="Adversary Surprise",
        description="Unexpected adversary actions and ambiguity.",
        parameters={"scenario_type": ScenarioType.ADVERSARY_SURPRISE.value},
    ),
]


# ═══════════════════════════════════════════════════════════════
# DEMO REGISTRY — Metadata for each of the five demos
# ═══════════════════════════════════════════════════════════════

class DemoID(str, Enum):
    LIVING_BRIEF = "demo1_living_brief"
    GRAYZONE_RBW = "demo2_grayzone_rbw"
    HIERARCHICAL_C2 = "demo3_hierarchical_c2"
    COUNTERFACTUAL_COA = "demo4_counterfactual_coa"
    AAR_DOCTRINAL_CLINIC = "demo5_aar_doctrinal_clinic"


@dataclass(frozen=True)
class DemoConfig:
    demo_id: DemoID
    title: str
    subtitle: str
    ooda_phases: Tuple[OODAPhase, ...]
    agent_roles: Tuple[str, ...]
    autogen_version: str  # "0.7" or "0.2"
    temperature: float = DEFAULT_TEMPERATURE
    max_messages: int = 5
    has_hitl: bool = False
    """True when the demo includes an interactive human-in-the-loop gate."""
    requires_explainability: bool = True
    """Every demo must include an Explainability Agent (RAI §3)."""


DEMOS: Dict[DemoID, DemoConfig] = {
    DemoID.LIVING_BRIEF: DemoConfig(
        demo_id=DemoID.LIVING_BRIEF,
        title="Living Scenario Brief",
        subtitle="Adaptive Situational Awareness Under Uncertainty",
        ooda_phases=(OODAPhase.OBSERVE, OODAPhase.ORIENT),
        agent_roles=(
            "Scenario Orchestrator",
            "ISR / Intel Fusion",
            "Assessment Agent",
            "Briefing / Explainer",
            "Commander (HITL)",
        ),
        autogen_version="0.7",
        temperature=0.3,
        max_messages=4,
        has_hitl=True,
    ),
    DemoID.GRAYZONE_RBW: DemoConfig(
        demo_id=DemoID.GRAYZONE_RBW,
        title="Maritime Gray-Zone Escalation Manager",
        subtitle="Red / Blue / White Cell Play",
        ooda_phases=(OODAPhase.ORIENT, OODAPhase.DECIDE, OODAPhase.ACT),
        agent_roles=(
            "Blue Planner",
            "Red Team",
            "White Cell / Umpire",
            "Legal / ROE",
            "Strategic Communications",
            "Explainability Agent",
        ),
        autogen_version="0.7",
        temperature=0.4,
        max_messages=5,
        has_hitl=True,
    ),
    DemoID.HIERARCHICAL_C2: DemoConfig(
        demo_id=DemoID.HIERARCHICAL_C2,
        title="Hierarchical Commander–Manager–Operator Agent Team",
        subtitle="Multi-Echelon Decision Decomposition with Hybrid Reasoning",
        ooda_phases=(OODAPhase.DECIDE, OODAPhase.ACT),
        agent_roles=(
            "Commander",
            "Surface Warfare Manager",
            "Air Warfare Manager",
            "Operator (×4)",
            "Multi-Model Selector",
            "Feedback Aggregator",
            "Explainability Agent",
        ),
        autogen_version="0.7",
        temperature=0.3,
        max_messages=5,
    ),
    DemoID.COUNTERFACTUAL_COA: DemoConfig(
        demo_id=DemoID.COUNTERFACTUAL_COA,
        title="Counterfactual COA Analysis",
        subtitle="Detecting Bias & Stress-Testing Decisions",
        ooda_phases=(OODAPhase.ORIENT, OODAPhase.DECIDE),
        agent_roles=(
            "COA Generator",
            "Adjudication Agent",
            "Counterfactual Perturbation Agent",
            "Bias / Feedback Auditor",
            "Explainability Agent",
        ),
        autogen_version="0.7",
        temperature=0.3,
        max_messages=5,
        has_hitl=True,
    ),
    DemoID.AAR_DOCTRINAL_CLINIC: DemoConfig(
        demo_id=DemoID.AAR_DOCTRINAL_CLINIC,
        title="After-Action Replay & Doctrinal Clinic",
        subtitle="Learning from the Game — Closing the OODA Loop",
        ooda_phases=(
            OODAPhase.OBSERVE,
            OODAPhase.ORIENT,
            OODAPhase.DECIDE,
            OODAPhase.ACT,
        ),
        agent_roles=(
            "Replay Narrator",
            "Doctrinal Critic",
            "Counterfactual Branch",
            "Lessons Learned Compiler",
            "Facilitator (HITL)",
            "Explainability Agent",
        ),
        autogen_version="0.7",
        temperature=0.3,
        max_messages=5,
        has_hitl=True,
    ),
}


# ═══════════════════════════════════════════════════════════════
# EXPANDED AGENT ROLES — Superset across all five demos
# ═══════════════════════════════════════════════════════════════

class AgentRole(str, Enum):
    # Command hierarchy (Demo 3)
    COMMANDER = "commander"
    MANAGER = "manager"
    OPERATOR = "operator"
    # Intel & assessment (Demo 1)
    ANALYST = "analyst"
    BRIEFER = "briefer"
    ORCHESTRATOR = "orchestrator"
    # Planning & review (Demos 2, 4, 5)
    PLANNER = "planner"
    REVIEWER = "reviewer"
    AUDITOR = "auditor"
    # Adversary / adjudication (Demo 2)
    RED_TEAM = "red_team"
    WHITE_CELL = "white_cell"
    LEGAL_ROE = "legal_roe"
    STRATCOMM = "stratcomm"
    # Cross-cutting (Demo 3)
    MODEL_SELECTOR = "model_selector"
    FEEDBACK_AGGREGATOR = "feedback_aggregator"
    # AAR (Demo 5)
    NARRATOR = "narrator"
    DOCTRINAL_CRITIC = "doctrinal_critic"
    COUNTERFACTUAL = "counterfactual"
    LESSONS_COMPILER = "lessons_compiler"
    # Cross-cutting Responsible AI roles
    EXPLAINER = "explainer"
    FACILITATOR_HITL = "facilitator_hitl"
    COMMANDER_HITL = "commander_hitl"


# ═══════════════════════════════════════════════════════════════
# ESCALATION LADDER — Shared by Demos 2 & 5
# ═══════════════════════════════════════════════════════════════

class EscalationLevel(str, Enum):
    ROUTINE = "ROUTINE"
    POSTURING = "POSTURING"
    PROVOCATION = "PROVOCATION"
    CONFRONTATION = "CONFRONTATION"
    CRISIS = "CRISIS"
    CONFLICT = "CONFLICT"


ESCALATION_LADDER: List[Dict[str, Any]] = [
    {"level": 0, "name": EscalationLevel.ROUTINE,       "threshold": 0,  "color": "#2ea043"},
    {"level": 1, "name": EscalationLevel.POSTURING,     "threshold": 3,  "color": "#7dc434"},
    {"level": 2, "name": EscalationLevel.PROVOCATION,   "threshold": 6,  "color": "#d4a72c"},
    {"level": 3, "name": EscalationLevel.CONFRONTATION, "threshold": 10, "color": "#db6d28"},
    {"level": 4, "name": EscalationLevel.CRISIS,        "threshold": 15, "color": "#da3633"},
    {"level": 5, "name": EscalationLevel.CONFLICT,      "threshold": 21, "color": "#8b0000"},
]


def get_escalation_level(index: int) -> Dict[str, Any]:
    """Return the escalation-ladder step for a given cumulative index."""
    result = ESCALATION_LADDER[0]
    for step in ESCALATION_LADDER:
        if index >= step["threshold"]:
            result = step
    return result


# ═══════════════════════════════════════════════════════════════
# ROE POSTURES — Shared by Demos 2 & 5
# ═══════════════════════════════════════════════════════════════

class ROEPosture(str, Enum):
    PEACETIME = "PEACETIME"
    ELEVATED = "ELEVATED"
    WEAPONS_FREE = "WEAPONS_FREE"


ROE_POSTURES: Dict[str, Dict[str, Any]] = {
    ROEPosture.PEACETIME: {
        "description": "Normal peacetime ROE. Defensive weapons release only.",
        "max_escalation": 6,
    },
    ROEPosture.ELEVATED: {
        "description": "Elevated threat ROE. Active self-defense authorized.",
        "max_escalation": 15,
    },
    ROEPosture.WEAPONS_FREE: {
        "description": "Weapons free within designated zone. Hostile act/intent criteria met.",
        "max_escalation": 999,
    },
}


# ═══════════════════════════════════════════════════════════════
# SCORING DIMENSIONS — Five-axis rubric (Demos 2 & 5)
# ═══════════════════════════════════════════════════════════════

class ScoringDimension(str, Enum):
    IMPACT = "impact"
    ESCALATION = "escalation"
    COMMUNICATION = "communication"
    POLITICAL = "political"
    RESOURCE = "resource"


SCORING_DIMENSIONS: List[str] = [d.value for d in ScoringDimension]

SCORE_RANGE: Tuple[int, int] = (-3, 3)  # min, max per dimension per action


# ═══════════════════════════════════════════════════════════════
# SIDES & UNIT TYPES — Shared by Demos 1, 2, 3
# ═══════════════════════════════════════════════════════════════

class Side(str, Enum):
    BLUE = "BLUE"
    RED = "RED"
    GRAY = "GRAY"  # Ambiguous / militia (Demo 1)


class UnitType(str, Enum):
    DDG = "DDG"
    FFG = "FFG"
    PATROL = "PC"
    MPA = "MPA"
    UAV = "UAV"
    SUB = "SSN"
    COAST_GUARD = "CCG"
    MILITIA = "MILITIA"


# ═══════════════════════════════════════════════════════════════
# TERRAIN — Grid terrain types for Demo 3
# ═══════════════════════════════════════════════════════════════

class Terrain(str, Enum):
    OPEN_WATER = "~"
    STRAIT = "="
    SHALLOWS = "."
    ISLAND = "#"
    PORT = "P"


# ═══════════════════════════════════════════════════════════════
# PER-DEMO RUNTIME DEFAULTS
# ═══════════════════════════════════════════════════════════════

# Demo 3 — grid wargame
GRID_SIZE: int = 10
NUM_WARGAME_TURNS: int = 3

# Demo 4 — counterfactual COA
NUM_COUNTERFACTUAL_WORLDS: int = 4
PERTURBATION_AXES: Tuple[str, ...] = (
    "weather",
    "unit_readiness",
    "adversary_intent",
    "roe_constraint",
)

# Demo 2 — gray-zone turns
NUM_GRAYZONE_TURNS: int = 5

# Demo 5 — AAR
DEMO2_LOG_FILENAME: str = "demo2_game_log.json"


# ═══════════════════════════════════════════════════════════════
# RESPONSIBLE AI HELPERS
# ═══════════════════════════════════════════════════════════════

def make_synthetic_world_state(
    scenario_name: str = "Unnamed Scenario",
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Return a minimal world-state dict pre-populated with RAI markers.

    Every world-state JSON produced by any demo **must** include the
    ``synthetic`` flag and ``disclaimer`` text required by the project's
    Responsible AI policy (§1 — Fully Synthetic Data Only).
    """
    state: Dict[str, Any] = {
        "synthetic": SYNTHETIC_DATA_MARKER,
        "disclaimer": SYNTHETIC_DATA_DISCLAIMER,
        "scenario_name": scenario_name,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    if extra:
        state.update(extra)
    return state


def build_agent_system_prompt(
    role_description: str,
    *,
    include_hitl: bool = True,
    include_doctrinal_disclaimer: bool = False,
) -> str:
    """Compose a system-message string that embeds RAI guardrails.

    Parameters
    ----------
    role_description:
        The agent-specific role and task instructions.
    include_hitl:
        When *True* (default), appends the HITL advisory so the agent
        frames outputs as recommendations, not directives (RAI §2).
    include_doctrinal_disclaimer:
        When *True*, appends the doctrinal-authority disclaimer (RAI §4).
    """
    parts = [role_description.rstrip()]
    if include_hitl:
        parts.append(HITL_SYSTEM_PROMPT)
    if include_doctrinal_disclaimer:
        parts.append(DOCTRINAL_DISCLAIMER)
    return "\n\n".join(parts)


def validate_demo_rai(demo: DemoConfig) -> List[str]:
    """Return a list of RAI-compliance warnings for *demo*.

    Checks performed:
    * Explainability agent presence (RAI §3)
    * HITL flag consistency with agent-role naming

    Returns an empty list when the demo passes all checks.
    """
    warnings: List[str] = []
    roles_lower = [r.lower() for r in demo.agent_roles]

    # §3 — Explainability agent required
    if demo.requires_explainability:
        has_explainer = any(
            "explain" in r or "briefing" in r for r in roles_lower
        )
        if not has_explainer:
            warnings.append(
                f"{demo.demo_id.value}: Missing Explainability Agent "
                f"(RAI §3 — every demo must include one)."
            )

    # §2 — HITL flag should match presence of a HITL role
    has_hitl_role = any("hitl" in r for r in roles_lower)
    if demo.has_hitl and not has_hitl_role:
        warnings.append(
            f"{demo.demo_id.value}: has_hitl=True but no agent role "
            f"name contains 'HITL'."
        )
    if has_hitl_role and not demo.has_hitl:
        warnings.append(
            f"{demo.demo_id.value}: Agent role contains 'HITL' but "
            f"has_hitl flag is False."
        )

    return warnings


def validate_all_demos_rai() -> List[str]:
    """Run :func:`validate_demo_rai` across the full demo registry."""
    warnings: List[str] = []
    for demo in DEMOS.values():
        warnings.extend(validate_demo_rai(demo))
    return warnings

