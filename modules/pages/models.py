import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.metrics import r2_score

C = {'bg':'#0D0F1A','card':'#13162B','purple':'#6C63FF',
     'cyan':'#00D4FF','coral':'#FF6B6B','amber':'#FFD93D',
     'green':'#6BCB77','text':'#E8EAF6','muted':'#8892B0'}

def render(artifacts):
    lb          = artifacts['leaderboard']
    all_results = artifacts['all_results']
    best_name   = artifacts['best_name']
    X_val       = artifacts['X_val']
    X_val_sc    = artifacts['X_val_sc']
    y_val       = artifacts['y_val']

    st.markdown("""
    <div class="page-header">
      <div class="page-title">🤖 Model Performance</div>
      <div class="page-subtitle">
        11 models trained, tuned, and compared honestly
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Leaderboard HTML table
    rows_html = ""
    for i, row in lb.iterrows():
        rank_class = f"rank-{i}" if i <= 3 else ""
        medal = "🥇" if i==1 else ("🥈" if i==2 else ("🥉" if i==3 else f"#{i}"))
        best_mark = " ⭐" if row['Model'] == best_name else ""
        rows_html += f"""
        <tr class="{rank_class}">
          <td>{medal}</td>
          <td>{row['Model']}{best_mark}</td>
          <td>{row['Family']}</td>
          <td>{row['Val R²']:.4f}</td>
          <td>{row['Val RMSE']:.4f}</td>
          <td>{row['Val MAE']:.4f}</td>
          <td>{row['CV R²']:.4f}</td>
          <td>{row['Test R²']:.4f}</td>
        </tr>"""

    st.markdown(f"""
    <div class="section-card">
      <div class="section-title">🏆 Model Leaderboard</div>
      <table class="lb-table">
        <thead><tr>
          <th>Rank</th><th>Model</th><th>Family</th>
          <th>Val R²</th><th>Val RMSE</th><th>Val MAE</th>
          <th>CV R²</th><th>Test R²</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

    # Actual vs Predicted for top 3
    st.markdown("""
    <div class="section-title" style="padding:8px 0 4px;">
        🎯 Actual vs Predicted — Top 3 Models
    </div>""", unsafe_allow_html=True)

    top3 = lb.head(3)['Model'].tolist()
    fig  = make_subplots(rows=1, cols=3,
             subplot_titles=[f'#{i+1}: {m}' for i, m in enumerate(top3)],
             horizontal_spacing=0.1)
    perfect = np.linspace(y_val.min()-1, y_val.max()+1, 100)

    for i, name in enumerate(top3):
        r    = all_results[name]
        Xvl  = X_val_sc if r['scaled'] else X_val
        pred = r['model'].predict(Xvl)
        err  = np.abs(y_val.values - pred)

        fig.add_trace(go.Scatter(
            x=y_val, y=pred, mode='markers',
            marker=dict(color=err,
                colorscale=[[0,C['green']],[0.5,C['amber']],[1,C['coral']]],
                size=6, opacity=0.8, showscale=(i==2),
                colorbar=dict(title='|Error|',
                    tickfont=dict(color=C['muted'],size=8),
                    len=0.4, thickness=8) if i==2 else None,
                line=dict(color=C['bg'],width=0.4)),
            showlegend=False,
            hovertemplate='Actual: %{x:.2f}<br>Pred: %{y:.2f}<extra></extra>',
        ), row=1, col=i+1)
        fig.add_trace(go.Scatter(
            x=perfect, y=perfect, mode='lines',
            line=dict(color=C['text'], width=1.5, dash='dash'),
            showlegend=False), row=1, col=i+1)
        fig.add_annotation(
            xref=f'x{i+1 if i>0 else ""} domain',
            yref=f'y{i+1 if i>0 else ""} domain',
            x=0.05, y=0.93,
            text=f"R²={r['val_r2']:.4f}",
            showarrow=False,
            font=dict(size=10, color=C['amber']),
            bgcolor=C['card'], borderpad=3, xanchor='left')

    fig.update_layout(
        paper_bgcolor=C['bg'], plot_bgcolor=C['card'],
        font=dict(color=C['text'], family='Inter', size=12),
        height=380, margin=dict(t=60,b=50,l=50,r=30))
    for a in fig['layout']['annotations'][:3]:
        a['font'] = dict(color=C['muted'], size=11)
    st.plotly_chart(fig, use_container_width=True)
