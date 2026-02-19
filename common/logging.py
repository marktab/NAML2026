"""Lightweight, notebook-friendly logging utilities.

Provides structured, HTML-styled log output for Jupyter notebooks.

Core levels:
    log_info      – general informational messages (blue)
    log_warning   – caution / non-fatal issues (amber)
    log_error     – failures and exceptions (red)
    log_success   – completion & ready-state confirmations (green)
    log_debug     – verbose diagnostic detail (gray)

Structured helpers:
    log_section   – phase / section headers with optional description
    log_step      – agent-activity or pipeline-step progress
    log_metric    – key-value metric reporting
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

try:
	from IPython.display import HTML, display
except Exception:  # pragma: no cover - IPython may not be present
	HTML = None
	display = None

# ── Colour palette ────────────────────────────────────────────
_COLORS: Dict[str, str] = {
	"INFO":    "#1f6feb",
	"WARN":    "#bf8700",
	"ERROR":   "#d73a49",
	"SUCCESS": "#2ea043",
	"DEBUG":   "#6e7781",
	"STEP":    "#8b949e",
	"SECTION": "#58a6ff",
	"METRIC":  "#d2a8ff",
}

# Rotating accent colours used by log_section when no explicit
# colour is supplied.  Indexed by (phase_num % len) so they cycle.
_SECTION_PALETTE = ["#58a6ff", "#d2a8ff", "#f0883e", "#2ea043", "#f778ba", "#db6d28"]

# ── Shared monospace font-family ──────────────────────────────
_FONT = (
	"ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "
	"'Liberation Mono', 'Courier New', monospace"
)


# ── Data structures ───────────────────────────────────────────
@dataclass
class LogEntry:
	level: str
	message: str
	timestamp: str
	extra: Dict[str, Any] = field(default_factory=dict)


_LOGS: List[LogEntry] = []


def _now_iso() -> str:
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _append(level: str, message: str, **extra: Any) -> LogEntry:
	entry = LogEntry(level=level, message=message, timestamp=_now_iso(),
	                 extra=extra if extra else {})
	_LOGS.append(entry)
	return entry


# ── HTML emitters ─────────────────────────────────────────────
def _emit_html(entry: LogEntry) -> None:
	"""Render a single-line log entry as styled HTML."""
	if display is None or HTML is None:
		return
	color = _COLORS.get(entry.level, "#6e7781")
	html = (
		f"<div style='font-family: {_FONT}; font-size: 12px;'>"
		f"<span style='color: {color}; font-weight: 600;'>[{entry.level}]</span> "
		f"<span style='color: #24292f;'>[{entry.timestamp}]</span> "
		f"<span style='color: #24292f;'>{entry.message}</span>"
		"</div>"
	)
	display(HTML(html))


def _emit_section_html(title: str, description: Optional[str], color: str) -> None:
	"""Render a phase / section header block."""
	if display is None or HTML is None:
		return
	desc_html = (
		f"<p style='margin:0; color:#8b949e;'>{description}</p>"
		if description else ""
	)
	html = (
		f"<div style='background:#0d1117; color:#c9d1d9; padding:16px; "
		f"border-radius:8px; margin:16px 0 8px 0; font-family:{_FONT}; "
		f"border-left:4px solid {color};'>"
		f"<h3 style='color:{color}; margin:0 0 8px 0;'>{title}</h3>"
		f"{desc_html}</div>"
	)
	display(HTML(html))


def _emit_step_html(agent: str, action: str) -> None:
	"""Render an agent / pipeline step progress line."""
	if display is None or HTML is None:
		return
	html = (
		f"<div style='font-family: {_FONT}; font-size: 12px; "
		f"padding: 2px 0;'>"
		f"<span style='color: #58a6ff; font-weight: 600;'>{agent}</span>"
		f"<span style='color: #6e7781;'> → </span>"
		f"<span style='color: #c9d1d9;'>{action}</span>"
		"</div>"
	)
	display(HTML(html))


def _emit_metric_html(label: str, value: Any, unit: Optional[str]) -> None:
	"""Render a key-value metric line."""
	if display is None or HTML is None:
		return
	unit_span = f" <span style='color:#8b949e;'>{unit}</span>" if unit else ""
	html = (
		f"<div style='font-family: {_FONT}; font-size: 12px; "
		f"padding: 2px 0;'>"
		f"<span style='color: #d2a8ff; font-weight: 600;'>[METRIC]</span> "
		f"<span style='color: #c9d1d9;'>{label}:</span> "
		f"<span style='color: #f0f6fc; font-weight: 600;'>{value}</span>"
		f"{unit_span}"
		"</div>"
	)
	display(HTML(html))


# ── Core log functions ────────────────────────────────────────
def log_info(message: str, *, show_html: bool = True) -> LogEntry:
	"""Log an informational message (blue)."""
	entry = _append("INFO", message)
	if show_html:
		_emit_html(entry)
	else:
		print(f"[INFO] [{entry.timestamp}] {entry.message}")
	return entry


def log_warning(message: str, *, show_html: bool = True) -> LogEntry:
	"""Log a warning message (amber)."""
	entry = _append("WARN", message)
	if show_html:
		_emit_html(entry)
	else:
		print(f"[WARN] [{entry.timestamp}] {entry.message}")
	return entry


def log_error(message: str, *, show_html: bool = True) -> LogEntry:
	"""Log an error message (red)."""
	entry = _append("ERROR", message)
	if show_html:
		_emit_html(entry)
	else:
		print(f"[ERROR] [{entry.timestamp}] {entry.message}")
	return entry


def log_success(message: str, *, show_html: bool = True) -> LogEntry:
	"""Log a success / completion / ready-state message (green)."""
	entry = _append("SUCCESS", message)
	if show_html:
		_emit_html(entry)
	else:
		print(f"[OK] [{entry.timestamp}] {entry.message}")
	return entry


def log_debug(message: str, *, show_html: bool = True) -> LogEntry:
	"""Log a verbose diagnostic message (gray)."""
	entry = _append("DEBUG", message)
	if show_html:
		_emit_html(entry)
	else:
		print(f"[DEBUG] [{entry.timestamp}] {entry.message}")
	return entry


# ── Structured helpers ────────────────────────────────────────
def log_section(
	title: str,
	description: Optional[str] = None,
	*,
	phase: Optional[int] = None,
	color: Optional[str] = None,
	show_html: bool = True,
) -> LogEntry:
	"""Log a phase / section header with optional description.

	Parameters
	----------
	title : str
	    Section heading text.  If *phase* is given, it is prepended
	    automatically (e.g. ``"Phase 2: Doctrinal Critique"``).
	description : str, optional
	    One-line subtitle rendered below the heading.
	phase : int, optional
	    Numeric phase index.  Drives automatic colour cycling and the
	    ``Phase N:`` prefix.
	color : str, optional
	    Explicit CSS colour override.  When omitted the colour is
	    picked from :data:`_SECTION_PALETTE` using *phase*.
	show_html : bool
	    Emit styled HTML (default) or fall back to plain text.
	"""
	display_title = f"Phase {phase}: {title}" if phase is not None else title
	resolved_color = color or (
		_SECTION_PALETTE[phase % len(_SECTION_PALETTE)]
		if phase is not None
		else _COLORS["SECTION"]
	)
	entry = _append("SECTION", display_title, description=description, phase=phase)
	if show_html:
		_emit_section_html(display_title, description, resolved_color)
	else:
		sep = "═" * 60
		print(f"\n{sep}")
		print(f"  {display_title}")
		if description:
			print(f"  {description}")
		print(sep)
	return entry


def log_step(
	agent: str,
	action: str,
	*,
	show_html: bool = True,
) -> LogEntry:
	"""Log an agent or pipeline-step progress update.

	Parameters
	----------
	agent : str
	    Name of the agent, component, or pipeline stage.
	action : str
	    Short description of what the agent is doing.
	"""
	message = f"{agent} → {action}"
	entry = _append("STEP", message, agent=agent, action=action)
	if show_html:
		_emit_step_html(agent, action)
	else:
		print(f"[STEP] [{entry.timestamp}] {message}")
	return entry


def log_metric(
	label: str,
	value: Any,
	unit: Optional[str] = None,
	*,
	show_html: bool = True,
) -> LogEntry:
	"""Log a key-value metric (e.g. counts, scores, durations).

	Parameters
	----------
	label : str
	    Metric name.
	value : Any
	    Metric value (number, string, etc.).
	unit : str, optional
	    Unit suffix (e.g. ``"ms"``, ``"%"``).
	"""
	display_msg = f"{label}: {value}" + (f" {unit}" if unit else "")
	entry = _append("METRIC", display_msg, label=label, value=value, unit=unit)
	if show_html:
		_emit_metric_html(label, value, unit)
	else:
		print(f"[METRIC] [{entry.timestamp}] {display_msg}")
	return entry


# ── Log management ────────────────────────────────────────────
def get_logs(*, level: Optional[str] = None) -> List[LogEntry]:
	"""Return collected log entries, optionally filtered by level."""
	if level is None:
		return list(_LOGS)
	level_upper = level.upper()
	return [e for e in _LOGS if e.level == level_upper]


def clear_logs() -> None:
	"""Discard all accumulated log entries."""
	_LOGS.clear()

