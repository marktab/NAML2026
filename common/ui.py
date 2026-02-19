"""UI helpers for notebook demos.

Provides shared HTML rendering utilities and ipywidgets helpers used across
all five NAML 2026 demo notebooks.  Extracted from inline display code so
that notebooks stay concise and visual styling remains consistent.

Responsible AI Alignment
------------------------
This module enforces several Responsible AI principles from the project's
RAI charter:

- **Synthetic-only framing** — ``render_synthetic_banner`` and
  ``render_scope_statement`` display mandatory disclaimers that all
  scenario data is artificial and the system carries no operational
  authority.
- **Human-in-the-Loop (HITL)** — ``render_hitl_gate`` renders a
  prominent visual gate reminding operators that a human decision is
  required before the workflow proceeds.
- **Explainability** — ``render_reasoning_trace`` surfaces transparent,
  inspectable agent reasoning traces so reviewers can audit *why* the
  system reached a conclusion.
- **Bias detection** — ``render_bias_card`` presents structured bias
  findings with named cognitive biases and confidence levels.

Sections
--------
**Theme constants** — dark-mode colour palette, shared CSS tokens, and the
canonical Responsible AI scope statement.

**Responsible AI helpers**:
    render_scope_statement  – RAI & scope disclaimer banner (all demos)
    render_synthetic_banner – synthetic-data notice (all demos)
    render_hitl_gate        – human-in-the-loop decision gate (Demos 1–5)
    render_reasoning_trace  – explainability trace card (Demos 1–5)
    render_bias_card        – structured bias finding card (Demo 4)

**HTML card / banner helpers** (pure ``display(HTML(...))``):
    render_turn_header    – per-turn header bar (Demos 1–3)
    render_escalation_banner – escalation callout between turns (Demos 1–3)
    render_phase_header   – numbered phase header with accent colour (Demo 5)
    render_agent_card     – agent output card with per-agent colour (Demo 5)
    render_commander_box  – green commander / facilitator input box (Demos 1, 2)
    render_info_box       – neutral info / instruction box (Demos 1–5)
    render_threshold_alert – escalation threshold-crossing alert (Demo 2)
    render_hr             – styled horizontal rule separator (Demos 1–3)

**Dashboard / table helpers**:
    render_scores_row_html – one ``<tr>`` of +/- colour-coded scores (Demo 2)
    render_dashboard       – scoring table + escalation bar (Demo 2)
    render_game_log_table  – full encounter summary table with bars (Demo 5)
    render_grid_html       – 10×10 battlespace grid (Demo 3)
    render_selector_summary – Multi-Model Selector dashboard (Demo 3)

**ipywidgets helpers** (import guarded):
    make_decision_widgets  – Accept / Reject toggle-buttons per COA (Demo 4)
"""

from __future__ import annotations

import html as _html
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Sequence, Tuple

try:
    from IPython.display import HTML, display
except Exception:  # pragma: no cover
    HTML = None  # type: ignore[assignment,misc]
    display = None  # type: ignore[assignment]

# ═══════════════════════════════════════════════════════════════
# THEME CONSTANTS
# ═══════════════════════════════════════════════════════════════

_FONT = (
    "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "
    "'Liberation Mono', 'Courier New', monospace"
)

# Dark-mode card backgrounds
BG_DARK = "#0d1117"
BG_CARD = "#161b22"
BG_TURN = "#1a1a2e"

# Text colours
FG_PRIMARY = "#c9d1d9"
FG_SECONDARY = "#8b949e"
FG_ACCENT = "#58a6ff"

# Side colours
COLOR_BLUE_SIDE = "#58a6ff"
COLOR_RED_SIDE = "#da3633"
COLOR_GREEN = "#2ea043"

# Escalation level colours (shared by Demos 2 & 5)
ESCALATION_COLORS: Dict[str, str] = {
    "ROUTINE": "#2ea043",
    "POSTURING": "#7dc434",
    "PROVOCATION": "#d4a72c",
    "CONFRONTATION": "#db6d28",
    "CRISIS": "#da3633",
    "CONFLICT": "#8b0000",
}

# Phase accent colours (Demo 5 / log_section; cycles by index)
PHASE_PALETTE: List[str] = [
    "#58a6ff", "#d2a8ff", "#f0883e", "#2ea043", "#f778ba", "#db6d28",
]

# Per-agent accent colours (Demo 5 AAR agents)
AGENT_COLORS: Dict[str, str] = {
    "Replay_Narrator": "#58a6ff",
    "Doctrinal_Critic": "#d2a8ff",
    "Counterfactual_Branch": "#f0883e",
    "Lessons_Compiler": "#2ea043",
}

# Bias confidence colours (Demo 4)
CONFIDENCE_COLORS: Dict[str, str] = {
    "high": "#d73a49",
    "medium": "#bf8700",
    "low": "#6e7781",
}

# Canonical Responsible AI scope statement (must appear in every notebook)
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

# Required disclaimer for world-state JSON and fixtures
SYNTHETIC_DISCLAIMER: str = (
    "All data is artificially generated for research and educational "
    "purposes only."
)

# Named cognitive biases used by the Bias Auditor (Demo 4)
COGNITIVE_BIASES: List[str] = [
    "anchoring",
    "recency bias",
    "escalation commitment",
    "mirror-imaging",
    "availability heuristic",
]


# ═══════════════════════════════════════════════════════════════
# RESPONSIBLE AI HELPERS
# ═══════════════════════════════════════════════════════════════

def render_scope_statement() -> None:
    """Display the Responsible AI & Scope Statement banner.

    Every notebook must call this once (typically near the top) to
    satisfy the project's RAI scope-statement compliance requirement.
    """
    display(HTML(
        f"<div style='background:#0d1117; color:#c9d1d9; padding:16px; "
        f"border-radius:8px; margin:16px 0; font-family:{_FONT}; "
        f"border:1px solid #f0883e; border-left:4px solid #f0883e;'>"
        f"<h4 style='color:#f0883e; margin:0 0 8px 0;'>"
        f"⚖ Responsible AI &amp; Scope Statement</h4>"
        f"<p style='margin:0; font-size:12px; line-height:1.6;'>"
        f"{_html.escape(SCOPE_STATEMENT)}</p></div>"
    ))


def render_synthetic_banner(
    context: str = "",
    *,
    border_color: str = "#d2a8ff",
) -> None:
    """Display a synthetic-data notice banner.

    Use at the start of any section that presents scenario content
    (world-state JSON, agent outputs, etc.) to reinforce the
    synthetic-only constraint.

    Parameters
    ----------
    context : str
        Optional qualifier, e.g. ``"World-State JSON"``.
    border_color : str
        Left-border accent colour.
    """
    prefix = f"{_html.escape(context)} — " if context else ""
    display(HTML(
        f"<div style='background:{BG_DARK}; color:{FG_SECONDARY}; "
        f"padding:8px 14px; margin:10px 0; border-left:3px solid {border_color}; "
        f"font-family:{_FONT}; font-size:11px;'>"
        f"🔬 {prefix}<em>{_html.escape(SYNTHETIC_DISCLAIMER)}</em></div>"
    ))


def render_hitl_gate(
    action_description: str,
    *,
    agent_name: str = "",
) -> None:
    """Display a human-in-the-loop decision gate banner.

    Renders a high-visibility box signalling that the system is
    pausing for a human decision.  Must appear before any
    ``input()`` / widget prompt that gates a consequential action.

    Parameters
    ----------
    action_description : str
        Plain-English description of the action awaiting human
        approval (e.g. ``"Accept or modify the recommended COA"``).
    agent_name : str
        Optional agent that produced the recommendation.
    """
    agent_line = (
        f"<div style='color:{FG_SECONDARY}; font-size:11px; margin-top:6px;'>"
        f"Recommendation provided by: <b>{_html.escape(agent_name)}</b> "
        f"— all decisions remain with the human operator.</div>"
    ) if agent_name else ""
    display(HTML(
        f"<div style='background:#1a2a1a; color:#b0ffb0; padding:14px; "
        f"border-radius:6px; margin:12px 0; font-family:{_FONT}; "
        f"border:2px solid {COLOR_GREEN};'>"
        f"<b>⏸ HUMAN DECISION REQUIRED</b><br>"
        f"{_html.escape(action_description)}"
        f"{agent_line}</div>"
    ))


def render_reasoning_trace(
    agent_name: str,
    reasoning_steps: Sequence[str],
    conclusion: str,
    *,
    accent: str = "",
) -> None:
    """Display an explainability / reasoning trace card.

    The Responsible AI charter requires every agent chain to
    terminate in a transparent explanation of *why* the system
    reached its conclusion.  This helper renders that trace in
    an inspectable, numbered-step format.

    Parameters
    ----------
    agent_name : str
        Agent that produced the trace.
    reasoning_steps : sequence of str
        Ordered reasoning steps (displayed as a numbered list).
    conclusion : str
        Final conclusion or recommendation text.
    accent : str
        Accent colour override — defaults to the agent's colour in
        ``AGENT_COLORS`` or ``FG_ACCENT``.
    """
    col = accent or AGENT_COLORS.get(agent_name, FG_ACCENT)
    steps_html = "".join(
        f"<li style='margin-bottom:4px;'>{_html.escape(s)}</li>"
        for s in reasoning_steps
    )
    display(HTML(
        f"<div style='background:{BG_CARD}; color:{FG_PRIMARY}; padding:16px; "
        f"border-radius:8px; margin:8px 0; font-family:{_FONT}; "
        f"border:1px solid #30363d; border-left:4px solid {col};'>"
        f"<div style='color:{col}; font-weight:bold; font-size:13px; "
        f"margin-bottom:8px;'>🔍 Reasoning Trace — {_html.escape(agent_name)}</div>"
        f"<ol style='margin:0 0 10px 18px; padding:0; font-size:12px; "
        f"line-height:1.7;'>{steps_html}</ol>"
        f"<div style='border-top:1px solid #30363d; padding-top:8px; "
        f"font-size:12px;'><b>Conclusion:</b> {_html.escape(conclusion)}</div>"
        f"</div>"
    ))


def render_bias_card(
    bias_name: str,
    confidence: str,
    evidence: str,
    appeal_brief: str,
    *,
    agent_name: str = "Bias_Auditor",
) -> None:
    """Display a structured bias-detection finding (Demo 4).

    The RAI charter requires bias outputs to name specific cognitive
    biases by their accepted terms and produce structured 'appeal
    briefs' rather than vague disclaimers.

    Parameters
    ----------
    bias_name : str
        Named cognitive bias (e.g. ``"anchoring"``,
        ``"recency bias"``, ``"mirror-imaging"``).
    confidence : str
        Confidence level — one of ``"high"``, ``"medium"``, ``"low"``.
    evidence : str
        Evidence passage supporting the finding.
    appeal_brief : str
        Structured appeal brief explaining how the bias
        may have influenced the analysis and suggested mitigations.
    agent_name : str
        Display name of the auditing agent.
    """
    conf_col = CONFIDENCE_COLORS.get(confidence.lower(), FG_SECONDARY)
    display(HTML(
        f"<div style='background:{BG_CARD}; color:{FG_PRIMARY}; padding:16px; "
        f"border-radius:8px; margin:8px 0; font-family:{_FONT}; "
        f"border:1px solid #30363d; border-left:4px solid {conf_col};'>"
        f"<div style='font-weight:bold; font-size:13px; margin-bottom:6px;'>"
        f"⚠ Bias Finding — <span style='color:{conf_col};'>"
        f"{_html.escape(bias_name.title())}</span>"
        f" <span style='font-size:11px; color:{conf_col};'>"
        f"[{_html.escape(confidence.upper())} confidence]</span></div>"
        f"<div style='font-size:12px; margin-bottom:8px;'>"
        f"<b>Agent:</b> {_html.escape(agent_name)}</div>"
        f"<div style='font-size:12px; margin-bottom:8px;'>"
        f"<b>Evidence:</b> {_html.escape(evidence)}</div>"
        f"<div style='border-top:1px solid #30363d; padding-top:8px; "
        f"font-size:12px;'><b>Appeal Brief:</b> "
        f"{_html.escape(appeal_brief)}</div></div>"
    ))


# ═══════════════════════════════════════════════════════════════
# HTML CARD / BANNER HELPERS
# ═══════════════════════════════════════════════════════════════

def render_turn_header(
    turn_num: int,
    dtg: str,
    subtitle: str = "",
    *,
    extra_html: str = "",
) -> None:
    """Display a per-turn header bar (dark-themed, monospace).

    Used by Demos 1, 2, and 3 at the start of each wargame turn.

    Parameters
    ----------
    turn_num : int
        Turn number (1-based).
    dtg : str
        Date-time group string (e.g. ``"081200ZFEB2026"``).
    subtitle : str
        Additional single-line info rendered below the header.
    extra_html : str
        Raw HTML appended inside the container (e.g. override notice).
    """
    sub = f"<br>{subtitle}" if subtitle else ""
    display(HTML(
        f"<div style='background:{BG_TURN}; color:#e0e0ff; padding:12px; "
        f"border-radius:6px; margin:8px 0; font-family:{_FONT};'>"
        f"<b>=== TURN {turn_num} — {_html.escape(dtg)} ===</b>"
        f"{sub}{extra_html}</div>"
    ))


def render_escalation_banner(message: str = "ESCALATION — PROCEEDING TO NEXT TURN") -> None:
    """Display a red-tinted escalation advance banner."""
    display(HTML(
        f"<div style='background:#2a1a1a; color:#ffb0b0; padding:12px; "
        f"border-radius:6px; margin:16px 0; font-family:{_FONT}; "
        f"text-align:center;'><b>{_html.escape(message)}</b></div>"
    ))


def render_phase_header(
    phase_num: int,
    title: str,
    description: str = "",
    *,
    color: Optional[str] = None,
) -> None:
    """Display a numbered phase header with accent colour (Demo 5 AAR phases).

    Parameters
    ----------
    phase_num : int
        Phase number (1-based).  Drives colour cycling when *color* is omitted.
    title : str
        Phase title text.
    description : str
        One-line subtitle rendered below the heading.
    color : str, optional
        Explicit CSS colour override.
    """
    resolved = color or PHASE_PALETTE[(phase_num - 1) % len(PHASE_PALETTE)]
    desc = (f"<p style='margin:0; color:{FG_SECONDARY};'>"
            f"{_html.escape(description)}</p>") if description else ""
    display(HTML(
        f"<div style='background:{BG_DARK}; color:{FG_PRIMARY}; padding:16px; "
        f"border-radius:8px; margin:16px 0 8px 0; font-family:{_FONT}; "
        f"border-left:4px solid {resolved};'>"
        f"<h2 style='color:{resolved}; margin:0 0 8px 0;'>"
        f"Phase {phase_num}: {_html.escape(title)}</h2>{desc}</div>"
    ))


def render_agent_card(agent_name: str, content: str) -> None:
    """Display an agent's output in a styled dark card (Demo 5 AAR).

    Agent outputs rendered here are **recommendations and analysis**,
    never orders or directives, consistent with the project's HITL
    requirement.

    Parameters
    ----------
    agent_name : str
        Agent name — used both as label and colour-key lookup.
    content : str
        Pre-formatted text (whitespace preserved via ``pre-wrap``).
    """
    col = AGENT_COLORS.get(agent_name, FG_SECONDARY)
    display(HTML(
        f"<div style='background:{BG_CARD}; color:{FG_PRIMARY}; padding:16px; "
        f"border-radius:8px; margin:8px 0; font-family:{_FONT}; "
        f"border:1px solid #30363d;'>"
        f"<div style='color:{col}; font-weight:bold; font-size:14px; "
        f"margin-bottom:8px; border-bottom:1px solid #30363d; "
        f"padding-bottom:6px;'>{_html.escape(agent_name)}</div>"
        f"<div style='white-space:pre-wrap; font-size:12px; "
        f"line-height:1.6;'>{content}</div></div>"
    ))


def render_commander_box(text: str, *, label: str = "COMMANDER") -> None:
    """Display a green-themed commander / facilitator input box.

    .. note:: RAI alignment

       This box renders the **human operator's** query or guidance —
       it does not represent an autonomous directive.  All agent
       responses framed around this input use advisory language
       ("recommends", "assesses", "suggests"), never directive
       language ("orders", "commands").

    Parameters
    ----------
    text : str
        The commander's query or override text.
    label : str
        Label prefix (e.g. ``"COMMANDER"``, ``"COMMANDER ORDERS"``).
    """
    display(HTML(
        f"<div style='background:#1a2a1a; color:#b0ffb0; padding:12px; "
        f"border-radius:6px; margin:8px 0; font-family:{_FONT};'>"
        f"<b>{_html.escape(label)}:</b> {_html.escape(text)}</div>"
    ))


def render_info_box(
    html_content: str,
    *,
    border_color: str = FG_ACCENT,
    background: str = BG_TURN,
    font_size: str = "11px",
) -> None:
    """Display a neutral information / instruction box.

    Parameters
    ----------
    html_content : str
        Inner HTML (may contain markup).
    border_color : str
        Left border accent colour.
    background : str
        Background colour.
    font_size : str
        CSS font-size value.
    """
    display(HTML(
        f"<div style='background:{background}; color:{FG_SECONDARY}; "
        f"padding:6px 12px; margin:12px 0; border-left:3px solid {border_color}; "
        f"font-family:{_FONT}; font-size:{font_size};'>{html_content}</div>"
    ))


def render_threshold_alert(
    prev_level: str,
    new_level: str,
    *,
    color: Optional[str] = None,
) -> None:
    """Display an escalation threshold-crossing alert (Demo 2).

    Parameters
    ----------
    prev_level : str
        Previous escalation level name.
    new_level : str
        New escalation level name.
    color : str, optional
        Override colour (defaults to ``ESCALATION_COLORS[new_level]``).
    """
    col = color or ESCALATION_COLORS.get(new_level, "#da3633")
    display(HTML(
        f"<div style='background:{col}33; border:2px solid {col}; color:#fff; "
        f"padding:12px; border-radius:6px; margin:8px 0; font-family:{_FONT}; "
        f"text-align:center; font-size:14px;'>"
        f"⚠ THRESHOLD CROSSING: {_html.escape(prev_level)} → "
        f"<b>{_html.escape(new_level)}</b></div>"
    ))


def render_hr() -> None:
    """Display a styled horizontal-rule separator."""
    display(HTML("<hr style='border:2px solid #4a4a6a; margin:16px 0;'>"))


def render_summary_card(
    title: str,
    body_html: str,
    *,
    accent: str = FG_ACCENT,
) -> None:
    """Display a dark-themed summary card with a coloured title.

    Useful for assessment-evolution summaries (Demo 1), hierarchy
    analysis (Demo 3), and similar wrap-up sections.

    Parameters
    ----------
    title : str
        Card heading.
    body_html : str
        Inner HTML rendered below the title.
    accent : str
        Title colour.
    """
    display(HTML(
        f"<div style='background:{BG_DARK}; color:{FG_PRIMARY}; padding:16px; "
        f"border-radius:8px; margin:16px 0; font-family:{_FONT};'>"
        f"<h3 style='color:{accent}; margin-top:0;'>{_html.escape(title)}</h3>"
        f"{body_html}</div>"
    ))


# ═══════════════════════════════════════════════════════════════
# DASHBOARD / TABLE HELPERS
# ═══════════════════════════════════════════════════════════════

def render_scores_row_html(
    label: str,
    scores: Dict[str, int],
    row_bg: str = "#0d1b2a",
) -> str:
    """Return one ``<tr>`` of +/− colour-coded scores (Demo 2 dashboard).

    Parameters
    ----------
    label : str
        Row label (e.g. ``"BLUE (cumulative)"``).
    scores : dict
        ``{dimension: int_value}`` mapping.
    row_bg : str
        Row background colour.

    Returns
    -------
    str
        HTML ``<tr>`` fragment.
    """
    cells = "".join(
        f"<td style='padding:4px 8px; text-align:center;'>"
        f"<span style='color:{COLOR_GREEN if v > 0 else COLOR_RED_SIDE if v < 0 else FG_SECONDARY};'>"
        f"{v:+d}</span></td>"
        for v in scores.values()
    )
    return (
        f"<tr style='background:{row_bg};'>"
        f"<td style='padding:4px 8px; font-weight:bold;'>"
        f"{_html.escape(label)}</td>{cells}</tr>"
    )


def render_dashboard(
    turn_num: int,
    blue_scores: Dict[str, int],
    red_scores: Dict[str, int],
    escalation_index: int,
    escalation_level: str,
    roe_posture: str,
) -> None:
    """Display the scoring dashboard and escalation status (Demo 2).

    Parameters
    ----------
    turn_num : int
        Current turn number.
    blue_scores, red_scores : dict
        Cumulative dimension scores for each side.
    escalation_index : int
        Current numeric escalation index.
    escalation_level : str
        Current escalation level name.
    roe_posture : str
        Current ROE posture name.
    """
    esc_color = ESCALATION_COLORS.get(escalation_level, FG_SECONDARY)
    dims = list(blue_scores.keys())
    header = "".join(
        f"<th style='padding:4px 8px;'>{d.title()}</th>" for d in dims
    )
    display(HTML(
        f"<div style='background:{BG_DARK}; color:{FG_PRIMARY}; padding:16px; "
        f"border-radius:8px; margin:8px 0; font-family:{_FONT};'>"
        f"<h3 style='color:{FG_ACCENT}; margin-top:0;'>Dashboard — Turn {turn_num}</h3>"
        f"<table style='border-collapse:collapse; width:100%; color:{FG_PRIMARY};'>"
        f"<tr style='border-bottom:1px solid #30363d;'>"
        f"<th style='padding:4px 8px; text-align:left;'>Side</th>{header}</tr>"
        f"{render_scores_row_html('BLUE (cumulative)', blue_scores, '#0d1b2a')}"
        f"{render_scores_row_html('RED (cumulative)', red_scores, '#1a0d0d')}"
        f"</table>"
        f"<div style='margin-top:12px; padding:8px; border-radius:4px; "
        f"background:{esc_color}22; border:1px solid {esc_color};'>"
        f"<b>ESCALATION:</b> {escalation_index} — <b>{_html.escape(escalation_level)}</b>"
        f" &nbsp;|&nbsp; <b>ROE:</b> {_html.escape(roe_posture)}"
        f"</div></div>"
    ))


def render_game_log_table(log: Dict[str, Any]) -> None:
    """Display the full encounter summary table with escalation bars (Demo 5).

    Parameters
    ----------
    log : dict
        Game log dict with keys ``scenario``, ``turns`` (list of turn dicts
        each containing ``turn``, ``dtg``, ``red_label``, ``blue_label``,
        ``escalation_delta``, ``escalation_index``, ``escalation_level``,
        ``threshold_crossing``, ``roe_posture``).
    """
    rows = ""
    for t in log["turns"]:
        esc = t["escalation_index"]
        level = t["escalation_level"]
        bar_width = min(esc * 12, 100)
        col = ESCALATION_COLORS.get(level, FG_SECONDARY)
        crossing = " ⚠" if t.get("threshold_crossing") else ""
        rows += (
            f"<tr>"
            f"<td style='padding:6px;'>{t['turn']}</td>"
            f"<td style='padding:6px;'>{t['dtg']}</td>"
            f"<td style='padding:6px; color:{COLOR_RED_SIDE};'>"
            f"{_html.escape(t['red_label'])}</td>"
            f"<td style='padding:6px; color:{COLOR_BLUE_SIDE};'>"
            f"{_html.escape(t['blue_label'])}</td>"
            f"<td style='padding:6px;'>{t['escalation_delta']:+d}</td>"
            f"<td style='padding:6px;'>"
            f"<div style='display:flex; align-items:center;'>"
            f"<div style='background:{col}; width:{bar_width}px; height:14px; "
            f"border-radius:3px; margin-right:6px;'></div>"
            f"<span style='color:{col};'>{esc} {_html.escape(level)}{crossing}</span>"
            f"</div></td>"
            f"<td style='padding:6px;'>{_html.escape(t['roe_posture'])}</td>"
            f"</tr>"
        )
    display(HTML(
        f"<div style='background:{BG_DARK}; color:{FG_PRIMARY}; padding:16px; "
        f"border-radius:8px; margin:8px 0; font-family:{_FONT};'>"
        f"<h3 style='color:{FG_ACCENT}; margin-top:0;'>"
        f"Game Log: {_html.escape(log['scenario'])}</h3>"
        f"<table style='border-collapse:collapse; width:100%; "
        f"color:{FG_PRIMARY}; font-size:12px;'>"
        f"<tr style='border-bottom:1px solid #30363d;'>"
        f"<th style='padding:6px;'>Turn</th><th style='padding:6px;'>DTG</th>"
        f"<th style='padding:6px;'>Red Action</th>"
        f"<th style='padding:6px;'>Blue Action</th>"
        f"<th style='padding:6px;'>Esc Δ</th>"
        f"<th style='padding:6px;'>Escalation</th>"
        f"<th style='padding:6px;'>ROE</th></tr>"
        f"{rows}</table></div>"
    ))


def render_grid_html(
    terrain_map: List[List[str]],
    unit_positions: Dict[Tuple[int, int], "Any"],
    *,
    grid_size: int = 10,
    terrain_colors: Optional[Dict[str, str]] = None,
) -> str:
    """Return an HTML ``<table>`` for a 2-D battlespace grid (Demo 3).

    Parameters
    ----------
    terrain_map : list[list[str]]
        2-D grid of terrain symbol strings.
    unit_positions : dict
        ``{(row, col): unit}`` mapping.  Each *unit* must expose
        ``.side`` (with ``.value`` ``"BLUE"`` or ``"RED"``) and
        a ``.symbol()`` method returning a short label string.
    grid_size : int
        Width/height of the grid.
    terrain_colors : dict, optional
        ``{terrain_symbol: css_colour}`` overrides.

    Returns
    -------
    str
        Complete ``<table>`` HTML string (caller should ``display(HTML(…))``.
    """
    default_colors: Dict[str, str] = {
        "~": "#1a3a5c",   # open water
        "=": "#2a5a8c",   # strait
        ".": "#3a6a5c",   # shallows
        "#": "#4a3a2a",   # island
        "P": "#5a4a3a",   # port
    }
    cmap = {**default_colors, **(terrain_colors or {})}

    html = ("<table style='border-collapse:collapse; font-family:monospace; "
            "font-size:13px;'><tr><td></td>")
    for c in range(grid_size):
        html += (f"<td style='text-align:center; padding:2px 6px; "
                 f"color:#888;'>{c}</td>")
    html += "</tr>"

    for r in range(grid_size):
        html += f"<tr><td style='padding:2px 6px; color:#888;'>{r}</td>"
        for c in range(grid_size):
            terrain = terrain_map[r][c]
            bg = cmap.get(terrain, BG_TURN)
            if (r, c) in unit_positions:
                u = unit_positions[(r, c)]
                fg = "#66bbff" if getattr(u, "side", None) and u.side.value == "BLUE" else "#ff6666"
                label = u.symbol()
            else:
                fg = "#555"
                label = terrain
            html += (
                f"<td style='background:{bg}; color:{fg}; text-align:center; "
                f"padding:4px 8px; border:1px solid #333; "
                f"font-weight:bold;'>{_html.escape(label)}</td>"
            )
        html += "</tr>"
    html += "</table>"
    return html


def render_selector_summary(
    selector_log: List[Dict[str, Any]],
    *,
    heuristic_color: str = "#7ee787",
    llm_color: str = "#ffa657",
) -> None:
    """Display the Multi-Model Selector decision dashboard (Demo 3).

    Parameters
    ----------
    selector_log : list[dict]
        List of dicts with keys ``turn``, ``unit``, ``complexity``,
        ``engine`` (``"HEURISTIC"`` or ``"LLM"``), and ``contacts``.
    heuristic_color, llm_color : str
        Accent colours for each engine type.
    """
    turns = sorted(set(d["turn"] for d in selector_log))

    rows_html = ""
    for d in selector_log:
        eng_color = heuristic_color if d["engine"] == "HEURISTIC" else llm_color
        rows_html += (
            f"<tr style='border-bottom:1px solid #21262d;'>"
            f"<td style='padding:6px;'>{d['turn']}</td>"
            f"<td style='padding:6px;'>{_html.escape(str(d['unit']))}</td>"
            f"<td style='padding:6px;'>{_html.escape(str(d['complexity']))}</td>"
            f"<td style='padding:6px; color:{eng_color}; font-weight:bold;'>"
            f"{_html.escape(d['engine'])}</td>"
            f"<td style='padding:6px;'>{d['contacts']}</td>"
            f"</tr>"
        )

    stats_html = ""
    for t in turns:
        td = [d for d in selector_log if d["turn"] == t]
        h_ct = sum(1 for d in td if d["engine"] == "HEURISTIC")
        l_ct = sum(1 for d in td if d["engine"] == "LLM")
        total = len(td)
        h_pct = (h_ct / total * 100) if total else 0
        l_pct = (l_ct / total * 100) if total else 0
        stats_html += (
            f"<div style='margin-top:8px;'>"
            f"<b>Turn {t}:</b> "
            f"<span style='color:{heuristic_color};'>"
            f"HEURISTIC: {h_ct} ({h_pct:.0f}%)</span> | "
            f"<span style='color:{llm_color};'>"
            f"LLM: {l_ct} ({l_pct:.0f}%)</span></div>"
        )

    display(HTML(
        f"<div style='background:{BG_DARK}; color:{FG_PRIMARY}; padding:16px; "
        f"border-radius:8px; margin:8px 0; font-family:{_FONT};'>"
        f"<h3 style='color:{FG_ACCENT}; margin-top:0;'>"
        f"Multi-Model Selector — Decision Summary</h3>"
        f"<table style='width:100%; border-collapse:collapse;'>"
        f"<tr style='border-bottom:1px solid #30363d;'>"
        f"<th style='text-align:left; padding:6px; color:{FG_SECONDARY};'>Turn</th>"
        f"<th style='text-align:left; padding:6px; color:{FG_SECONDARY};'>Unit</th>"
        f"<th style='text-align:left; padding:6px; color:{FG_SECONDARY};'>Complexity</th>"
        f"<th style='text-align:left; padding:6px; color:{FG_SECONDARY};'>Engine</th>"
        f"<th style='text-align:left; padding:6px; color:{FG_SECONDARY};'>Contacts</th>"
        f"</tr>{rows_html}</table>{stats_html}"
        f"<div style='margin-top:12px; color:{FG_SECONDARY}; font-size:11px;'>"
        f"Green = cheap scripted heuristic (fast, deterministic). "
        f"Orange = LLM reasoning (flexible, handles novelty). "
        f"The same architecture swaps engines based on context — "
        f"demonstrating portability.</div></div>"
    ))


# ═══════════════════════════════════════════════════════════════
# IPYWIDGETS HELPERS (guarded import)
# ═══════════════════════════════════════════════════════════════

try:
    import ipywidgets as widgets
    from IPython.display import clear_output as _clear_output

    @dataclass
    class DemoUI:
        """Legacy scenario-selector UI for any demo that needs a
        dropdown + start / reset pattern."""

        scenario_dropdown: Any  # widgets.Dropdown
        start_button: Any  # widgets.Button
        reset_button: Any  # widgets.Button
        status: Any  # Optional[widgets.HTML]
        container: Any  # widgets.VBox

        def display(self) -> None:
            display(self.container)

    def build_demo_ui(
        scenarios: Sequence[str],
        on_start: Callable[[str], None],
        on_reset: Callable[[], None],
        *,
        show_status: bool = True,
        status_text: str = "Ready",
        start_label: str = "Start",
        reset_label: str = "Reset",
    ) -> DemoUI:
        """Build a scenario-selector UI with start / reset buttons."""
        scenario_dropdown = widgets.Dropdown(
            options=list(scenarios),
            description="Scenario:",
            layout=widgets.Layout(width="360px"),
        )
        start_button = widgets.Button(
            description=start_label,
            button_style="success",
            tooltip="Run the selected scenario",
        )
        reset_button = widgets.Button(
            description=reset_label,
            button_style="warning",
            tooltip="Reset demo state",
        )
        status_widget: Any = None
        if show_status:
            status_widget = widgets.HTML(
                value=f"<b>Status:</b> {status_text}",
                layout=widgets.Layout(margin="4px 0 0 0"),
            )

        def _handle_start(_btn: Any) -> None:
            on_start(str(scenario_dropdown.value))

        def _handle_reset(_btn: Any) -> None:
            on_reset()

        start_button.on_click(_handle_start)
        reset_button.on_click(_handle_reset)

        controls = widgets.HBox([scenario_dropdown, start_button, reset_button])
        children: list = [controls]
        if status_widget is not None:
            children.append(status_widget)
        container = widgets.VBox(children)

        return DemoUI(
            scenario_dropdown=scenario_dropdown,
            start_button=start_button,
            reset_button=reset_button,
            status=status_widget,
            container=container,
        )

    def make_decision_widgets(
        coas: List[Dict[str, Any]],
        world_label: str,
        decision_store: Dict[str, str],
    ) -> Tuple[List[Any], Any]:
        """Build Accept / Reject toggle-buttons per COA (Demo 4).

        Parameters
        ----------
        coas : list[dict]
            COA dicts, each with at least ``"id"`` and ``"name"`` keys.
        world_label : str
            Display label for the world (e.g. ``"Baseline"``).
        decision_store : dict
            Mutable dict that will be populated with
            ``{coa_id: "accept"|"reject"}`` as the user interacts.

        Returns
        -------
        tuple[list[HBox], Button]
            ``(rows, confirm_button)`` — caller composes into a ``VBox``.
        """
        rows: List[Any] = []
        for coa in coas:
            toggle = widgets.ToggleButtons(
                options=["Accept", "Reject"],
                description=f"{coa['id']}:",
                button_style="",
                tooltips=[f"Accept {coa['name']}", f"Reject {coa['name']}"],
                style={"description_width": "80px"},
            )

            def _on_change(change: Dict, coa_id: str = coa["id"]) -> None:
                decision_store[coa_id] = change["new"].lower()

            toggle.observe(_on_change, names="value")
            decision_store[coa["id"]] = "accept"  # default
            rows.append(widgets.HBox([
                toggle,
                widgets.HTML(f"  <i>{_html.escape(coa['name'])}</i>"),
            ]))

        confirm = widgets.Button(
            description=f"Confirm {world_label} Decisions",
            button_style="success",
            layout=widgets.Layout(width="320px"),
        )
        return rows, confirm

except ImportError:
    # ipywidgets not installed — widget helpers unavailable
    widgets = None  # type: ignore[assignment]
    _clear_output = None  # type: ignore[assignment]

