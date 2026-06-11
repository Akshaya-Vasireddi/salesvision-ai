# ============================================================
# styles.py — All custom CSS for SalesVision AI
# ============================================================

import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Root & Reset ── */
    :root {
        --bg:        #0D0F1A;
        --card:      #13162B;
        --card2:     #1A1E35;
        --border:    #2A2F4E;
        --purple:    #6C63FF;
        --cyan:      #00D4FF;
        --coral:     #FF6B6B;
        --amber:     #FFD93D;
        --green:     #6BCB77;
        --text:      #E8EAF6;
        --muted:     #8892B0;
        --pink:      #FF6B9D;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background-color: var(--card) !important;
        border-right: 1px solid var(--border) !important;
    }

    [data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    /* ── Hide Streamlit defaults ── */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }

    /* ── Sidebar logo ── */
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0 16px;
    }
    .logo-icon  { font-size: 28px; }
    .logo-text  { font-size: 20px; font-weight: 700;
                  color: var(--text); letter-spacing: -0.3px; }
    .logo-ai    { color: var(--purple); }

    .sidebar-divider {
        height: 1px;
        background: var(--border);
        margin: 8px 0;
    }

    /* ── Radio nav ── */
    [data-testid="stRadio"] label {
        padding: 8px 12px !important;
        border-radius: 8px !important;
        margin-bottom: 2px !important;
        cursor: pointer !important;
        transition: background 0.2s !important;
        font-size: 14px !important;
        color: var(--muted) !important;
    }
    [data-testid="stRadio"] label:hover {
        background: var(--card2) !important;
        color: var(--text) !important;
    }
    [data-testid="stRadio"] [aria-checked="true"] {
        background: rgba(108,99,255,0.15) !important;
        color: var(--purple) !important;
        font-weight: 500 !important;
    }

    /* ── Model badge ── */
    .model-badge {
        background: rgba(108,99,255,0.1);
        border: 1px solid rgba(108,99,255,0.3);
        border-radius: 10px;
        padding: 12px 14px;
    }
    .badge-label { font-size: 10px; color: var(--muted);
                   text-transform: uppercase; letter-spacing: 1px; }
    .badge-name  { font-size: 15px; font-weight: 600;
                   color: var(--text); margin: 4px 0 2px; }
    .badge-score { font-size: 12px; color: var(--green); }

    /* ── Page header ── */
    .page-header {
        padding: 8px 0 28px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 28px;
    }
    .page-title {
        font-size: 28px; font-weight: 700;
        color: var(--text); letter-spacing: -0.5px;
        margin: 0; line-height: 1.2;
    }
    .page-subtitle {
        font-size: 14px; color: var(--muted);
        margin: 6px 0 0;
    }

    /* ── KPI cards ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 28px;
    }
    .kpi-card {
        background: var(--card);
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid var(--border);
        transition: transform 0.2s, border-color 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: var(--purple);
    }
    .kpi-icon   { font-size: 22px; margin-bottom: 10px; }
    .kpi-value  { font-size: 28px; font-weight: 700;
                  color: var(--text); letter-spacing: -0.5px; line-height: 1; }
    .kpi-label  { font-size: 11px; color: var(--muted);
                  text-transform: uppercase; letter-spacing: 0.8px;
                  margin-top: 6px; }
    .kpi-delta  { font-size: 11px; margin-top: 4px; }

    /* ── Section cards ── */
    .section-card {
        background: var(--card);
        border-radius: 14px;
        padding: 22px 24px;
        border: 1px solid var(--border);
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 16px; font-weight: 600;
        color: var(--text); margin: 0 0 16px;
    }

    /* ── Insight boxes ── */
    .insight-box {
        background: var(--card2);
        border-left: 3px solid var(--purple);
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin: 12px 0;
        font-size: 13px;
        line-height: 1.7;
        color: var(--text);
    }
    .insight-box.green  { border-color: var(--green); }
    .insight-box.amber  { border-color: var(--amber); }
    .insight-box.coral  { border-color: var(--coral); }

    /* ── Prediction result card ── */
    .pred-result {
        background: linear-gradient(135deg,
            rgba(108,99,255,0.15), rgba(0,212,255,0.08));
        border: 1px solid rgba(108,99,255,0.4);
        border-radius: 16px;
        padding: 28px 32px;
        text-align: center;
        margin: 20px 0;
    }
    .pred-label  { font-size: 12px; color: var(--muted);
                   text-transform: uppercase; letter-spacing: 1px; }
    .pred-value  { font-size: 52px; font-weight: 700;
                   color: var(--cyan); letter-spacing: -2px;
                   line-height: 1.1; margin: 8px 0; }
    .pred-unit   { font-size: 16px; color: var(--muted); }
    .pred-conf   { font-size: 13px; color: var(--green); margin-top: 8px; }

    /* ── Metric row ── */
    .metric-row {
        display: flex; gap: 12px; margin: 16px 0;
    }
    .metric-pill {
        background: var(--card2);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px; color: var(--muted);
    }
    .metric-pill span { color: var(--text); font-weight: 500; }

    /* ── Leaderboard table ── */
    .lb-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .lb-table th {
        background: var(--card2); color: var(--muted);
        font-weight: 500; font-size: 11px;
        text-transform: uppercase; letter-spacing: 0.6px;
        padding: 10px 14px; text-align: left;
        border-bottom: 1px solid var(--border);
    }
    .lb-table td {
        padding: 10px 14px;
        border-bottom: 1px solid rgba(42,47,78,0.5);
        color: var(--text);
    }
    .lb-table tr:hover td { background: rgba(108,99,255,0.05); }
    .rank-1 td:first-child { color: var(--amber) !important;
                              font-weight: 600; }
    .rank-2 td:first-child { color: var(--muted); }
    .rank-3 td:first-child { color: var(--coral); }

    /* ── Sliders & inputs ── */
    [data-testid="stSlider"] > div > div > div {
        background: var(--purple) !important;
    }
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background: var(--purple) !important;
        border-color: var(--cyan) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: var(--purple) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        transition: opacity 0.2s !important;
        width: 100%;
    }
    .stButton > button:hover {
        opacity: 0.85 !important;
    }

    /* ── Optimizer result cards ── */
    .opt-card {
        background: var(--card);
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid var(--border);
        text-align: center;
    }
    .opt-channel { font-size: 22px; margin-bottom: 6px; }
    .opt-amount  { font-size: 26px; font-weight: 700; color: var(--text); }
    .opt-pct     { font-size: 12px; color: var(--muted); margin-top: 4px; }

    /* ── Report section ── */
    .report-block {
        background: var(--card);
        border-radius: 12px;
        padding: 20px 24px;
        border: 1px solid var(--border);
        margin-bottom: 16px;
        font-size: 13px;
        line-height: 1.8;
    }
    .report-title {
        font-size: 14px; font-weight: 600;
        color: var(--cyan); margin-bottom: 10px;
    }

    /* ── Plotly chart containers ── */
    .js-plotly-plot { border-radius: 12px; overflow: hidden; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--card); }
    ::-webkit-scrollbar-thumb { background: var(--border);
                                  border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)
