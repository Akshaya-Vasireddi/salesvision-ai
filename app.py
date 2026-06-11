# ============================================================
# SALESVISION AI — app.py
# Main Streamlit application entry point
# ============================================================

import streamlit as st

st.set_page_config(
    page_title="SalesVision AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports ──────────────────────────────────────────────────
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.optimize import minimize
from scipy import stats
import pickle, warnings, os, sys

warnings.filterwarnings('ignore')
sys.path.append('/content/salesvision')

from modules.styles   import inject_css
from modules.data     import load_all_artifacts
from modules.charts   import (plot_scatter_regression,
                               plot_correlation_heatmap,
                               plot_distributions,
                               plot_3d_scatter,
                               plot_revenue_surface)
from modules.predict  import (make_prediction,
                               run_budget_optimizer,
                               run_whatif)
from modules.explain  import (plot_global_importance,
                               plot_waterfall_chart,
                               plot_beeswarm)
from modules.bi       import render_bi_dashboard

# ── Load artifacts ───────────────────────────────────────────
artifacts = load_all_artifacts()

# ── Inject custom CSS ────────────────────────────────────────
inject_css()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">🎯</span>
        <span class="logo-text">SalesVision<span class="logo-ai"> AI</span></span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        options=[
            "🏠  Overview",
            "📊  EDA & Insights",
            "🤖  Model Performance",
            "🔍  Explainable AI",
            "🎯  Predict Sales",
            "💡  Budget Optimizer",
            "🔀  What-If Simulator",
            "📋  Executive Report",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    # Model badge
    best_name = artifacts['best_name']
    best_r2   = artifacts['all_results'][best_name]['test_r2']
    st.markdown(f"""
    <div class="model-badge">
        <div class="badge-label">Active Model</div>
        <div class="badge-name">{best_name}</div>
        <div class="badge-score">Test R² = {best_r2:.4f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("SalesVision AI v1.0 · Built with Streamlit")

# ── Route pages ──────────────────────────────────────────────
if   "Overview"    in page: from modules.pages.overview   import render; render(artifacts)
elif "EDA"         in page: from modules.pages.eda         import render; render(artifacts)
elif "Model"       in page: from modules.pages.models      import render; render(artifacts)
elif "Explainable" in page: from modules.pages.xai         import render; render(artifacts)
elif "Predict"     in page: from modules.pages.predict     import render; render(artifacts)
elif "Budget"      in page: from modules.pages.optimizer   import render; render(artifacts)
elif "What-If"     in page: from modules.pages.whatif      import render; render(artifacts)
elif "Executive"   in page: from modules.pages.report      import render; render(artifacts)
