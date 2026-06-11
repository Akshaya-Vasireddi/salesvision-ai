import streamlit as st
import plotly.graph_objects as go
from modules.predict import run_whatif

C = {'bg':'#0D0F1A','card':'#13162B','purple':'#6C63FF',
     'cyan':'#00D4FF','coral':'#FF6B6B','amber':'#FFD93D',
     'green':'#6BCB77','text':'#E8EAF6','muted':'#8892B0'}

def render(artifacts):
    df = artifacts['df']

    st.markdown("""
    <div class="page-header">
      <div class="page-title">🔀 What-If Simulator</div>
      <div class="page-subtitle">
        Adjust each channel's budget and see predicted
        sales impact instantly
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("""
        <div class="section-card">
          <div class="section-title">📥 Base Budget</div>
        """, unsafe_allow_html=True)

        base_tv   = st.number_input("📺 Base TV ($K)",
                                     0.0, 300.0,
                                     float(df['TV'].mean()), 1.0)
        base_rad  = st.number_input("📻 Base Radio ($K)",
                                     0.0, 50.0,
                                     float(df['Radio'].mean()), 0.5)
        base_news = st.number_input("📰 Base Newspaper ($K)",
                                     0.0, 115.0,
                                     float(df['Newspaper'].mean()), 0.5)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card" style="margin-top:12px;">
          <div class="section-title">🎛️ Adjust Spend (%)</div>
        """, unsafe_allow_html=True)

        tv_d    = st.slider("TV change (%)",   -80, 100, 0, 5)
        rad_d   = st.slider("Radio change (%)",-80, 100, 0, 5)
        news_d  = st.slider("Newspaper change (%)", -80, 100, 0, 5)

        sim_btn = st.button("▶ Run Simulation")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if sim_btn:
            result = run_whatif(
                base_tv, base_rad, base_news,
                tv_d, rad_d, news_d, artifacts
            )
            base  = result['base_sales']
            new   = result['new_sales']
            delta = result['delta']
            pct   = result['pct_change']
            color = C['green'] if delta >= 0 else C['coral']
            arrow = "↑" if delta >= 0 else "↓"

            st.markdown(f"""
            <div style="display:grid;
                        grid-template-columns:1fr 1fr;
                        gap:12px; margin-bottom:16px;">
              <div class="section-card" style="text-align:center;">
                <div class="kpi-label">Base Sales</div>
                <div class="kpi-value">${base:.2f}K</div>
              </div>
              <div class="section-card" style="text-align:center;
                border-color:{color}40;">
                <div class="kpi-label">New Sales</div>
                <div class="kpi-value"
                     style="color:{color};">${new:.2f}K</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="insight-box {'green' if delta>=0 else 'coral'}">
              <b>Impact Summary</b><br>
              Sales change: <b style="color:{color};">
              {arrow}{abs(delta):.3f}K ({arrow}{abs(pct):.1f}%)</b><br>
              TV: ${base_tv:.1f}K → ${result['new_tv']:.1f}K
              ({tv_d:+d}%)<br>
              Radio: ${base_rad:.1f}K → ${result['new_radio']:.1f}K
              ({rad_d:+d}%)<br>
              Newspaper: ${base_news:.1f}K →
              ${result['new_news']:.1f}K ({news_d:+d}%)
            </div>
            """, unsafe_allow_html=True)

            # Waterfall comparison
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Base', 'Change', 'New'],
                y=[base, delta, new],
                marker=dict(color=[C['cyan'],
                    C['green'] if delta>=0 else C['coral'],
                    C['purple']],
                    opacity=0.85,
                    line=dict(color=C['bg'], width=1)),
                text=[f'${v:.2f}K' for v in [base, delta, new]],
                textposition='outside',
                textfont=dict(color=C['text'], size=11),
                hovertemplate='%{x}: $%{y:.2f}K<extra></extra>',
            ))
            fig.update_layout(
                paper_bgcolor=C['bg'], plot_bgcolor=C['card'],
                font=dict(color=C['text'], family='Inter', size=12),
                height=300, margin=dict(t=30,b=40,l=50,r=30),
                yaxis=dict(gridcolor='#1E2340', zeroline=False,
                           tickfont=dict(color=C['muted'])),
                xaxis=dict(tickfont=dict(color=C['text'])),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style="height:380px; display:flex;
                        align-items:center; justify-content:center;
                        background:#13162B; border-radius:14px;
                        border:1px dashed #2A2F4E;">
              <div style="text-align:center; color:#8892B0;">
                <div style="font-size:40px; margin-bottom:12px;">🔀</div>
                <div style="font-size:14px;">
                    Adjust sliders and run simulation
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
