import streamlit as st
from modules.explain import (plot_global_importance,
                              plot_waterfall_chart,
                              plot_beeswarm)

def render(artifacts):
    shap_data  = artifacts['shap_data']
    X_tr_shap  = artifacts['X_tr_shap']
    X_vl_shap  = artifacts['X_vl_shap']
    y_val      = artifacts['y_val']
    best_name  = artifacts['best_name']

    st.markdown(f"""
    <div class="page-header">
      <div class="page-title">🔍 Explainable AI</div>
      <div class="page-subtitle">
        SHAP analysis for {best_name} —
        every prediction fully explained
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "🎯 Global Importance",
        "🐝 Beeswarm",
        "🔍 Waterfall",
    ])

    with tab1:
        st.plotly_chart(
            plot_global_importance(shap_data, X_tr_shap),
            use_container_width=True)
        st.markdown("""
        <div class="insight-box">
          Mean |SHAP| measures each feature's average absolute
          contribution to predictions. TV and TV×Radio dominate —
          confirming that TV spend and its synergy with Radio
          are the primary revenue levers.
        </div>""", unsafe_allow_html=True)

    with tab2:
        st.plotly_chart(
            plot_beeswarm(shap_data, X_tr_shap),
            use_container_width=True)
        st.markdown("""
        <div class="insight-box amber">
          Each dot is one campaign. Red = high feature value,
          Blue = low. TV shows a clear positive relationship —
          high TV spend always pushes predictions up.
          Newspaper shows minimal spread — low predictive power.
        </div>""", unsafe_allow_html=True)

    with tab3:
        fig, pred, actual = plot_waterfall_chart(
            shap_data, X_vl_shap, y_val)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""
        <div class="insight-box green">
          Waterfall for median campaign:
          Prediction = <b>${pred:.2f}K</b> |
          Actual = <b>${actual:.2f}K</b> |
          Error = <b>${abs(pred-actual):.2f}K</b><br>
          Each bar shows exactly how much each feature
          pushed the prediction above or below the baseline.
        </div>""", unsafe_allow_html=True)
