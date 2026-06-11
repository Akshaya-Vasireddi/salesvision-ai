import streamlit as st
import plotly.graph_objects as go
import numpy as np

def render(artifacts):
    df = artifacts['df']

    st.markdown("""
    <div class="page-header">
      <div class="page-title">🎯 SalesVision AI</div>
      <div class="page-subtitle">
        Intelligent Marketing & Revenue Optimization Platform
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI cards
    total_budget = df['TV'].mean()+df['Radio'].mean()+df['Newspaper'].mean()
    best_name    = artifacts['best_name']
    test_r2      = artifacts['all_results'][best_name]['test_r2']
    test_rmse    = artifacts['all_results'][best_name]['test_rmse']

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon">📊</div>
        <div class="kpi-value">{len(df)}</div>
        <div class="kpi-label">Campaigns Analysed</div>
        <div class="kpi-delta" style="color:#6BCB77">Full dataset</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-value">${df['Sales'].mean():.2f}K</div>
        <div class="kpi-label">Avg Sales Revenue</div>
        <div class="kpi-delta" style="color:#6BCB77">
            Max: ${df['Sales'].max():.1f}K
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">🤖</div>
        <div class="kpi-value">{test_r2:.4f}</div>
        <div class="kpi-label">Model Test R²</div>
        <div class="kpi-delta" style="color:#6BCB77">{best_name}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">🎯</div>
        <div class="kpi-value">±{test_rmse:.2f}K</div>
        <div class="kpi-label">Prediction Accuracy</div>
        <div class="kpi-delta" style="color:#6BCB77">RMSE on test set</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # What the platform does
    st.markdown("""
    <div class="section-card">
      <div class="section-title">Platform Capabilities</div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    caps = [
        ("📊", "EDA & Insights",
         "Distributions, correlations, and budget analysis"),
        ("🤖", "Model Comparison",
         "11 models benchmarked with honest validation"),
        ("🔍", "Explainable AI",
         "SHAP values — every prediction explained"),
        ("💡", "Budget Optimizer",
         "scipy.optimize finds the best spend allocation"),
    ]
    for col, (icon, title, desc) in zip(cols, caps):
        with col:
            st.markdown(f"""
            <div style="background:#1A1E35; border-radius:10px;
                        padding:16px; text-align:center;
                        border:1px solid #2A2F4E; height:130px;">
              <div style="font-size:26px; margin-bottom:8px;">{icon}</div>
              <div style="font-size:13px; font-weight:600;
                          color:#E8EAF6;">{title}</div>
              <div style="font-size:11px; color:#8892B0;
                          margin-top:6px; line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Key findings
    tv_corr   = df['TV'].corr(df['Sales'])
    rad_corr  = df['Radio'].corr(df['Sales'])
    news_corr = df['Newspaper'].corr(df['Sales'])

    st.markdown(f"""
    <div class="insight-box green">
      <b>🔑 Key Findings from {len(df)} campaigns</b><br>
      • TV is the dominant sales driver — Pearson r = {tv_corr:.3f}
        (explains {tv_corr**2*100:.1f}% of sales variance)<br>
      • Radio is a meaningful secondary channel — r = {rad_corr:.3f}<br>
      • Newspaper shows weak ROI signal — r = {news_corr:.3f}<br>
      • Best model ({best_name}) achieves R² = {test_r2:.4f} on unseen data
    </div>
    """, unsafe_allow_html=True)
