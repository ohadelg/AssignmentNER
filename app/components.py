"""
components.py
─────────────
Reusable HTML snippet builders for custom UI elements.

Every function returns a **self-contained** HTML string — no orphaned opening
or closing tags. This is critical because each st.markdown() call is rendered
as its own isolated DOM fragment by Streamlit.
"""

from __future__ import annotations

import pandas as pd

from config import BADGE_PALETTE


# ── Badge helpers ──────────────────────────────────────────────────────────────

def _badge_colors(class_name: str) -> tuple[str, str]:
    """Deterministically pick a (foreground, background) color pair for a class."""
    idx = abs(hash(class_name)) % len(BADGE_PALETTE)
    return BADGE_PALETTE[idx]


# ── Hero header ────────────────────────────────────────────────────────────────

def hero_header() -> str:
    return """
    <div class="hero-header">
        <div class="hero-badge">🔐 Powered by SecureBERT-NER</div>
        <h1 class="hero-title">Secure Entity Extractor</h1>
        <p class="hero-sub">
            Cybersecurity Named Entity Recognition —
            upload a threat report and extract structured intelligence
        </p>
    </div>
    <hr class="glow-divider">
    """


# ── Summary stat cards ─────────────────────────────────────────────────────────

def stat_cards(unique_classes: int, unique_entities: int, total_mentions: int) -> str:
    return f"""
    <div class="stats-row">
        <div class="stat-card blue">
            <div class="stat-value">{unique_classes}</div>
            <div class="stat-desc">Entity Classes Detected</div>
        </div>
        <div class="stat-card purple">
            <div class="stat-value">{unique_entities}</div>
            <div class="stat-desc">Unique Entities Found</div>
        </div>
        <div class="stat-card green">
            <div class="stat-value">{total_mentions}</div>
            <div class="stat-desc">Total Entity Mentions</div>
        </div>
    </div>
    """


# ── Entity table (self-contained, wrapped in its own section card) ────────────

def entity_report_section(df: pd.DataFrame) -> str:
    """
    Build a complete, self-contained report section card containing the
    entity table. No orphaned tags.
    """
    rows: list[str] = []
    for _, row in df.iterrows():
        fg, bg = _badge_colors(row["Class"])
        rows.append(
            f'<tr>'
            f'<td><span class="badge" style="color:{fg};background:{bg};">{row["Class"]}</span></td>'
            f'<td style="color:#94a3b8;">{row["Description"]}</td>'
            f'<td><span class="entity-text">{row["Entity"]}</span></td>'
            f'<td><span class="count-badge">{row["Count"]}</span></td>'
            f'</tr>'
        )

    body = "\n".join(rows)
    return f"""
    <div class="report-section">
        <div class="report-section-title">
            <span class="icon">📋</span> Entity Extraction Report
        </div>
        <div class="entity-table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Class</th>
                <th>Description</th>
                <th>Entity</th>
                <th>Count</th>
              </tr>
            </thead>
            <tbody>{body}</tbody>
          </table>
        </div>
    </div>"""


def chart_section_header() -> str:
    """Just the header label for the chart section (self-contained div)."""
    return """
    <div class="report-section" style="padding-bottom:0.5rem;">
        <div class="report-section-title">
            <span class="icon">📊</span> Entity Distribution
        </div>
    </div>"""


# ── File info line ─────────────────────────────────────────────────────────────

def file_info(name: str, size: int) -> str:
    return (
        f"<p style='color:#64748b;font-size:0.85rem;margin:0.6rem 0 0;'>"
        f"📄 <b style='color:#94a3b8'>{name}</b> — {size:,} bytes</p>"
    )


# ── Empty / placeholder states ─────────────────────────────────────────────────

def empty_state() -> str:
    return """
    <div style="text-align:center;padding:4rem 0 3rem;opacity:0.35;">
        <div style="font-size:3.5rem;margin-bottom:1rem;">🔍</div>
        <p style="color:#64748b;font-size:0.95rem;">
            Upload a cybersecurity document to begin entity extraction
        </p>
    </div>
    """


def no_filter_results() -> str:
    return "<p style='color:#64748b;text-align:center;padding:1rem;'>No results match your filter.</p>"
