"""
charts.py
─────────
Plotly chart factory functions.

SOLID notes
───────────
S – Single Responsibility: owns only chart construction. No Streamlit calls,
    no data processing, no CSS.
O – Open / Closed: to add a new chart type, add a new function here.
    Existing functions and callers remain untouched.

Each function accepts a pre-aggregated DataFrame (output of
entity_processor.aggregate) and returns a go.Figure ready for
st.plotly_chart().
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from config import ENTITY_META, FALLBACK_COLOR

# ── Shared layout defaults ─────────────────────────────────────────────────────
_TRANSPARENT = "rgba(0,0,0,0)"
_TICK_FONT   = dict(family="JetBrains Mono", size=11, color="#94a3b8")
# margin is intentionally excluded here so each chart can set its own
# without causing a duplicate-keyword-argument error on **_BASE_LAYOUT unpacking.
_BASE_LAYOUT = dict(
    plot_bgcolor=_TRANSPARENT,
    paper_bgcolor=_TRANSPARENT,
    font=dict(family="Inter", color="#94a3b8"),
    height=380,
)


def _class_colors(classes: pd.Series) -> list[str]:
    """Map a Series of class names to their configured accent colors."""
    return [ENTITY_META.get(c, {}).get("color", FALLBACK_COLOR) for c in classes]


def _class_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total mention count per class, sorted descending."""
    return (
        df.groupby("Class")["Count"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


# ── Bar chart ──────────────────────────────────────────────────────────────────

def bar_chart(df: pd.DataFrame) -> go.Figure:
    """Vertical bar chart: one bar per entity class, height = total mentions."""
    totals = _class_totals(df)
    colors = _class_colors(totals["Class"])

    fig = go.Figure(
        go.Bar(
            x=totals["Class"],
            y=totals["Count"],
            marker=dict(color=colors, opacity=0.85, line=dict(width=0)),
            text=totals["Count"],
            textposition="outside",
            textfont=dict(color="#94a3b8", size=11, family="JetBrains Mono"),
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        **_BASE_LAYOUT,
        margin=dict(l=0, r=0, t=20, b=0),
        showlegend=False,
        bargap=0.35,
        xaxis=dict(tickfont=_TICK_FONT, gridcolor="rgba(255,255,255,0.04)",
                   linecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(tickfont=_TICK_FONT, gridcolor="rgba(255,255,255,0.05)",
                   linecolor="rgba(255,255,255,0.08)", zeroline=False),
    )
    return fig


# ── Donut chart ────────────────────────────────────────────────────────────────

def donut_chart(df: pd.DataFrame) -> go.Figure:
    """Donut chart: slice per entity class, proportional to total mentions."""
    totals = _class_totals(df)
    colors = _class_colors(totals["Class"])
    labels = [
        f"{c} – {ENTITY_META.get(c, {}).get('label', c)}"
        for c in totals["Class"]
    ]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=totals["Count"],
            hole=0.6,
            marker=dict(colors=colors, line=dict(color="#0a0e1a", width=2)),
            textinfo="percent",
            textfont=dict(size=11, family="Inter"),
            hovertemplate="<b>%{label}</b><br>%{value} entities (%{percent})<extra></extra>",
        )
    )
    fig.update_layout(
        **_BASE_LAYOUT,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(font=dict(size=10, color="#94a3b8"),
                    bgcolor=_TRANSPARENT, itemsizing="constant"),
    )
    return fig
