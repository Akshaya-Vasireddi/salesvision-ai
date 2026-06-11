import streamlit as st
from modules.charts import (plot_scatter_regression,
                             plot_correlation_heatmap,
                             plot_distributions,
                             plot_3d_scatter,
                             plot_revenue_surface)

def render(artifacts):
    df = artifacts['df']

    st.markdown("""
    <div class="page-header">
      <div class="page-title">📊 EDA & Insights</div>
      <div class="page-subtitle">
        Exploratory analysis — distributions, correlations,
        and budget-sales relationships
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Distributions",
        "🔗 Correlations",
        "📡 Regression",
        "🌌 3D Views",
    ])

    with tab1:
        st.plotly_chart(plot_distributions(df),
                        use_container_width=True)
        st.markdown("""
        <div class="insight-box">
          TV budget is right-skewed — a few high-spend campaigns
          pull the mean up. Radio and Newspaper are more uniformly
          distributed. Sales is approximately normal (Shapiro-Wilk p > 0.05).
        </div>""", unsafe_allow_html=True)

    with tab2:
        st.plotly_chart(plot_correlation_heatmap(df),
                        use_container_width=True)
        st.markdown("""
        <div class="insight-box amber">
          TV–Sales r = 0.901 (p &lt; 0.001) — strongest signal.<br>
          Newspaper–Sales r = 0.158 — weakest, high variance.<br>
          Low inter-feature correlation confirms no multicollinearity concern.
        </div>""", unsafe_allow_html=True)

    with tab3:
        st.plotly_chart(plot_scatter_regression(df),
                        use_container_width=True)
        st.markdown("""
        <div class="insight-box green">
          Shaded bands show 95% confidence intervals on the OLS fit.
          TV has the tightest band — most consistent predictor.
          Newspaper has wide scatter — high uncertainty at all spend levels.
        </div>""", unsafe_allow_html=True)

    with tab4:
        view = st.radio("Select 3D view",
                        ["Campaign Space (TV × Radio × Sales)",
                         "Revenue Response Surface"],
                        horizontal=True)
        if "Campaign" in view:
            st.plotly_chart(plot_3d_scatter(df),
                            use_container_width=True)
        else:
            st.plotly_chart(plot_revenue_surface(df),
                            use_container_width=True)
