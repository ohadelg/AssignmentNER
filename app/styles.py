"""
styles.py
─────────
All custom CSS for the application, isolated in one place.

To change the color scheme, font, or layout: edit this file only.
No other module imports or embeds CSS.
"""

APP_CSS: str = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0e1a; color: #e2e8f0; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1400px; }

/* ── Hero Header ── */
.hero-header { text-align: center; padding: 3rem 0 2rem; }
.hero-title {
    font-size: 3.2rem; font-weight: 700;
    background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 50%, #00ff88 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -0.02em; margin: 0; line-height: 1.15;
}
.hero-sub {
    color: #64748b; font-size: 1.05rem; margin-top: 0.6rem;
    letter-spacing: 0.04em; font-weight: 400;
}
.hero-badge {
    display: inline-block; background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3); color: #00d4ff;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; padding: 0.3rem 0.9rem;
    border-radius: 100px; margin-bottom: 1.2rem;
}

/* ── Divider ── */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #00d4ff44, #7c3aed44, transparent);
    margin: 1.5rem 0 2.5rem; border: none;
}

/* ── Upload Card ── */
.upload-card {
    background: rgba(15,23,42,0.8); border: 1px solid rgba(0,212,255,0.15);
    border-radius: 16px; padding: 2rem 2.5rem;
    box-shadow: 0 0 40px rgba(0,212,255,0.04);
    backdrop-filter: blur(10px); margin-bottom: 1.5rem;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(0,212,255,0.3) !important;
    border-radius: 12px !important; background: rgba(0,212,255,0.03) !important;
    transition: border-color 0.3s ease, background 0.3s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,212,255,0.6) !important;
    background: rgba(0,212,255,0.06) !important;
}
[data-testid="stFileUploadDropzone"] { color: #94a3b8 !important; }

/* ── Button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    color: #ffffff !important; font-weight: 600; font-size: 1.05rem;
    letter-spacing: 0.05em; border: none !important; border-radius: 10px !important;
    padding: 0.75rem 2rem !important; cursor: pointer;
    transition: opacity 0.2s ease, transform 0.15s ease;
    box-shadow: 0 4px 24px rgba(0,212,255,0.25);
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.92; transform: translateY(-1px);
    box-shadow: 0 8px 32px rgba(0,212,255,0.4);
}
div[data-testid="stButton"] > button:active { transform: translateY(0); }

/* ── Labels ── */
.section-label {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: #00d4ff; margin-bottom: 0.4rem;
}

/* ── Stat Cards ── */
.stats-row { display: flex; gap: 1rem; margin-bottom: 2rem; }
.stat-card {
    flex: 1; background: rgba(15,23,42,0.9);
    border: 1px solid rgba(255,255,255,0.07); border-radius: 12px;
    padding: 1.3rem 1.5rem; text-align: center;
    position: relative; overflow: hidden;
}
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
.stat-card.blue::before   { background: linear-gradient(90deg, #00d4ff, #0099bb); }
.stat-card.purple::before { background: linear-gradient(90deg, #7c3aed, #a855f7); }
.stat-card.green::before  { background: linear-gradient(90deg, #00ff88, #00cc6a); }
.stat-value {
    font-size: 2.4rem; font-weight: 700;
    font-family: 'JetBrains Mono', monospace; line-height: 1;
}
.stat-card.blue   .stat-value { color: #00d4ff; }
.stat-card.purple .stat-value { color: #a855f7; }
.stat-card.green  .stat-value { color: #00ff88; }
.stat-desc { font-size: 0.78rem; color: #64748b; margin-top: 0.35rem; font-weight: 500; }

/* ── Report Sections ── */
.report-section {
    background: rgba(15,23,42,0.8); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 1.8rem 2rem; margin-bottom: 1.5rem;
    box-shadow: 0 2px 20px rgba(0,0,0,0.3);
}
.report-section-title {
    font-size: 1.05rem; font-weight: 600; color: #e2e8f0;
    margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.5rem;
}
.report-section-title .icon { font-size: 1.15rem; }

/* ── Entity Table ── */
.entity-table-wrapper {
    overflow-x: auto; border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.06);
}
table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
thead th {
    background: rgba(0,212,255,0.08); color: #00d4ff;
    font-weight: 600; font-size: 0.72rem; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 0.9rem 1rem; text-align: left;
    border-bottom: 1px solid rgba(0,212,255,0.15);
}
tbody tr {
    border-bottom: 1px solid rgba(255,255,255,0.04);
    transition: background 0.15s ease;
}
tbody tr:hover { background: rgba(0,212,255,0.04); }
tbody tr:last-child { border-bottom: none; }
tbody td { padding: 0.75rem 1rem; color: #cbd5e1; vertical-align: middle; }
.badge {
    display: inline-block; font-size: 0.7rem; font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    padding: 0.2rem 0.6rem; border-radius: 6px; letter-spacing: 0.06em;
}
.count-badge {
    display: inline-flex; align-items: center; justify-content: center;
    min-width: 2rem; height: 1.6rem; padding: 0 0.6rem;
    background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.25);
    color: #00d4ff; font-weight: 700; font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem; border-radius: 6px;
}
.entity-text {
    font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #e2e8f0;
}

/* ── Progress ── */
.stProgress > div > div { background: linear-gradient(90deg, #00d4ff, #7c3aed) !important; }

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; border-left-width: 3px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }
</style>
"""
