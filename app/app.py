"""
app.py
──────
Entry point and orchestration layer for Secure Entity Extractor.

Run with:
    streamlit run app/app.py
"""

import streamlit as st

import charts
import components
import entity_processor
from config import PAGE_ICON, PAGE_TITLE
from ner_service import SecureBertNERProvider
from styles import APP_CSS

# ── Page configuration (must be the first Streamlit call) ─────────────────────
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject global CSS ──────────────────────────────────────────────────────────
st.markdown(APP_CSS, unsafe_allow_html=True)

# ── Hero header ────────────────────────────────────────────────────────────────
st.markdown(components.hero_header(), unsafe_allow_html=True)

# ── Upload section ─────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    label="Drop a .txt file here or click to browse",
    type=["txt"],
    label_visibility="collapsed",
)

analyse_clicked = False
if uploaded_file:
    col_info, col_btn = st.columns([3, 1])
    with col_info:
        st.markdown(
            components.file_info(uploaded_file.name, uploaded_file.size),
            unsafe_allow_html=True,
        )
    with col_btn:
        analyse_clicked = st.button("⚡ Analyse", use_container_width=True)
else:
    if "df" in st.session_state:
        del st.session_state["df"]
        del st.session_state["stats"]
        del st.session_state["file_name"]
    st.markdown(
        "<p style='color:#334155;font-size:0.82rem;margin-top:0.5rem;text-align:center;'>"
        "Supported format: plain text (.txt)</p>",
        unsafe_allow_html=True,
    )

# ── Run analysis (only on button click) ───────────────────────────────────────
if analyse_clicked and uploaded_file is not None:
    raw_text = uploaded_file.read().decode("utf-8", errors="replace").strip()

    if not raw_text:
        st.warning("The uploaded file appears to be empty.")
        st.stop()

    with st.spinner("Loading SecureBERT-NER model…"):
        ner = SecureBertNERProvider()

    progress = st.progress(0, text="Extracting entities…")

    def _update_progress(current: int, total: int) -> None:
        pct = int(current / total * 100)
        progress.progress(pct, text=f"Extracting entities… chunk {current}/{total}")

    raw_entities = ner.extract(raw_text, on_chunk=_update_progress)
    progress.progress(100, text="Done!")
    progress.empty()

    if not raw_entities:
        st.info("No named entities were detected in the provided text.")
        st.stop()

    st.session_state["df"] = entity_processor.aggregate(raw_entities)
    st.session_state["stats"] = entity_processor.summary_stats(st.session_state["df"])
    st.session_state["file_name"] = uploaded_file.name

# ── Display results (persists across reruns thanks to session_state) ──────────
if "df" in st.session_state:
    df = st.session_state["df"]
    stats = st.session_state["stats"]
    file_name = st.session_state["file_name"]

    # ── Summary cards ──────────────────────────────────────────────────────
    st.markdown(
        components.stat_cards(
            stats["unique_classes"],
            stats["unique_entities"],
            stats["total_mentions"],
        ),
        unsafe_allow_html=True,
    )

    # ── Part 1: Search filter (Streamlit widget, placed BEFORE the HTML) ──
    search = st.text_input(
        "Filter entities…",
        placeholder="Search by entity text, class, or description…",
        label_visibility="collapsed",
    )
    filtered_df = entity_processor.filter_by_query(df, search)

    # ── Entity table (single self-contained HTML block) ────────────────────
    if filtered_df.empty:
        st.markdown(components.no_filter_results(), unsafe_allow_html=True)
    else:
        st.markdown(
            components.entity_report_section(filtered_df),
            unsafe_allow_html=True,
        )

    # ── Part 2: Distribution charts ────────────────────────────────────────
    st.markdown(components.chart_section_header(), unsafe_allow_html=True)

    tab_bar, tab_donut = st.tabs(["Bar Chart", "Donut Chart"])
    with tab_bar:
        st.plotly_chart(
            charts.bar_chart(df),
            width="stretch",
            config={"displayModeBar": False},
        )
    with tab_donut:
        st.plotly_chart(
            charts.donut_chart(df),
            width="stretch",
            config={"displayModeBar": False},
        )

    # ── CSV download ───────────────────────────────────────────────────────
    st.download_button(
        label="⬇  Download report as CSV",
        data=df.to_csv(index=False).encode(),
        file_name=f"entities_{file_name.removesuffix('.txt')}.csv",
        mime="text/csv",
        use_container_width=True,
    )

elif not uploaded_file:
    st.markdown(components.empty_state(), unsafe_allow_html=True)
