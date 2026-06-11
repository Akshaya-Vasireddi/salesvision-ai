import streamlit as st
import plotly.graph_objects as go
import numpy as np
from modules.predict import make_prediction

C = {'bg':'#0D0F1A','card':'#13162B','purple':'#6C63FF',
     'cyan':'#00D4FF','coral':'#FF6B6B','amber':'#FFD93D',
     'green':'#6BCB77','text':'#E8EAF6','muted':'#8892B0'}

def render(artifacts):
    df = artifacts['df']

    st.markdown("""
    <div class="page-header">
      <div class="page-title">🎯 Predict Sales</div>
      <div class="page-subtitle">
        Enter your advertising budget to get an AI sales prediction
        with confidence interval
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class="section-card">
          <div class="section-title">📥 Enter Budget</div>
        """, unsafe_allow_html=True)

        tv        = st.slider("📺 TV Budget ($K)",
                               0.0, 300.0, float(df['TV'].mean()),    0.5)
        radio     = st.slider("📻 Radio Budget ($K)",
                               0.0, 50.0,  float(df['Radio'].mean()), 0.5)
        newspaper = st.slider("📰 Newspaper Budget ($K)",
                               0.0, 115.0, float(df['Newspaper'].mean()), 0.5)

        total = tv + radio + newspaper
        st.markdown(f"""
        <div class="metric-row">
          <div class="metric-pill">
              Total spend: <span>${total:.1f}K</span>
          </div>
          <div class="metric-pill">
              TV share: <span>{tv/total*100:.0f}%</span>
          </div>
          <div class="metric-pill">
              Radio share: <span>{radio/total*100:.0f}%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        predict_btn = st.button("🚀 Predict Sales")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if predict_btn:
            with st.spinner("Computing prediction..."):
                result = make_prediction(tv, radio, newspaper, artifacts)

            pred  = result['prediction']
            lower = result['lower_ci']
            upper = result['upper_ci']
            conf  = result['confidence']

            st.markdown(f"""
            <div class="pred-result">
              <div class="pred-label">Predicted Sales Revenue</div>
              <div class="pred-value">${pred:.2f}K</div>
              <div class="pred-unit">thousands</div>
              <div class="pred-conf">
                  95% CI: [${lower:.2f}K — ${upper:.2f}K]
              </div>
            </div>
            """, unsafe_allow_html=True)

            avg_sales = float(df['Sales'].mean())
            delta     = pred - avg_sales
            arrow     = "↑" if delta >= 0 else "↓"
            color     = C['green'] if delta >= 0 else C['coral']

            st.markdown(f"""
            <div class="insight-box {'green' if delta>=0 else 'coral'}">
              <b>Prediction vs Dataset Average</b><br>
              Average campaign sales: ${avg_sales:.2f}K<br>
              Your prediction: ${pred:.2f}K
              (<span style="color:{color}">{arrow}
              {abs(delta):.2f}K, {abs(delta/avg_sales*100):.1f}%
              </span> vs average)<br>
              Confidence score: {conf:.1f}%
            </div>
            """, unsafe_allow_html=True)

            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pred,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Predicted Sales ($K)",
                       'font': {'color': C['text'], 'size': 14}},
                number={'suffix': 'K',
                        'font': {'color': C['cyan'], 'size': 32}},
                gauge={
                    'axis': {'range': [0, 30],
                             'tickcolor': C['muted'],
                             'tickfont': {'color': C['muted']}},
                    'bar':  {'color': C['purple']},
                    'bgcolor': C['card'],
                    'bordercolor': C['bg'],
                    'steps': [
                        {'range': [0,  10], 'color': '#1a0a0a'},
                        {'range': [10, 20], 'color': '#0a1a0a'},
                        {'range': [20, 30], 'color': '#0a1a1a'},
                    ],
                    'threshold': {
                        'line': {'color': C['amber'], 'width': 3},
                        'thickness': 0.75,
                        'value': avg_sales,
                    },
                },
            ))
            fig.update_layout(
                paper_bgcolor=C['bg'],
                font=dict(color=C['text'], family='Inter'),
                height=260, margin=dict(t=30,b=10,l=30,r=30))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style="height:400px; display:flex;
                        align-items:center; justify-content:center;
                        background:#13162B; border-radius:14px;
                        border:1px dashed #2A2F4E;">
              <div style="text-align:center; color:#8892B0;">
                <div style="font-size:40px; margin-bottom:12px;">🎯</div>
                <div style="font-size:14px;">
                    Adjust sliders and click Predict
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
