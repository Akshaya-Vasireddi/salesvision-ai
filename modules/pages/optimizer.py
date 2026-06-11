import streamlit as st
import plotly.graph_objects as go
from modules.predict import run_budget_optimizer

C = {'bg':'#0D0F1A','card':'#13162B','purple':'#6C63FF',
     'cyan':'#00D4FF','coral':'#FF6B6B','amber':'#FFD93D',
     'green':'#6BCB77','text':'#E8EAF6','muted':'#8892B0'}

def render(artifacts):
    st.markdown("""
    <div class="page-header">
      <div class="page-title">💡 Budget Optimizer</div>
      <div class="page-subtitle">
        Enter your total budget — AI finds the optimal
        TV / Radio / Newspaper split to maximise predicted sales
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.4])

    with col1:
        st.markdown("""
        <div class="section-card">
          <div class="section-title">⚙️ Optimization Settings</div>
        """, unsafe_allow_html=True)

        total = st.slider("💰 Total Budget ($K)",
                           10.0, 400.0, 200.0, 5.0)
        st.markdown(f"""
        <div style="color:#8892B0; font-size:12px; margin:8px 0 16px;">
          Budget range: $10K — $400K<br>
          Algorithm: SLSQP multi-start optimization
        </div>
        """, unsafe_allow_html=True)
        run_btn = st.button("⚡ Optimize Allocation")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if run_btn:
            with st.spinner("Running optimizer..."):
                result = run_budget_optimizer(total, artifacts)

            tv    = result['tv']
            radio = result['radio']
            news  = result['newspaper']
            pred  = result['predicted']

            # Allocation cards
            st.markdown(f"""
            <div style="display:grid;
                        grid-template-columns:repeat(3,1fr);
                        gap:12px; margin-bottom:16px;">
              <div class="opt-card">
                <div class="opt-channel">📺</div>
                <div class="opt-amount"
                     style="color:#00D4FF;">${tv:.1f}K</div>
                <div class="opt-pct">{result['tv_pct']:.1f}% of budget</div>
              </div>
              <div class="opt-card">
                <div class="opt-channel">📻</div>
                <div class="opt-amount"
                     style="color:#FFD93D;">${radio:.1f}K</div>
                <div class="opt-pct">{result['radio_pct']:.1f}% of budget</div>
              </div>
              <div class="opt-card">
                <div class="opt-channel">📰</div>
                <div class="opt-amount"
                     style="color:#FF6B6B;">${news:.1f}K</div>
                <div class="opt-pct">{result['news_pct']:.1f}% of budget</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="pred-result">
              <div class="pred-label">Expected Sales at Optimal Allocation</div>
              <div class="pred-value">${pred:.2f}K</div>
            </div>
            """, unsafe_allow_html=True)

            # Donut chart
            fig = go.Figure(go.Pie(
                labels=['TV', 'Radio', 'Newspaper'],
                values=[tv, radio, news],
                hole=0.55,
                marker=dict(colors=[C['cyan'], C['amber'], C['coral']],
                            line=dict(color=C['bg'], width=3)),
                textfont=dict(color=C['text'], size=12),
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>${%{value:.1f}}K<extra></extra>',
            ))
            fig.update_layout(
                paper_bgcolor=C['bg'],
                font=dict(color=C['text'], family='Inter'),
                height=280, margin=dict(t=20,b=10,l=10,r=10),
                annotations=[dict(
                    text=f'${total:.0f}K<br>Total',
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=14, color=C['text']))],
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div style="height:360px; display:flex;
                        align-items:center; justify-content:center;
                        background:#13162B; border-radius:14px;
                        border:1px dashed #2A2F4E;">
              <div style="text-align:center; color:#8892B0;">
                <div style="font-size:40px; margin-bottom:12px;">💡</div>
                <div style="font-size:14px;">
                    Set your budget and click Optimize
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
