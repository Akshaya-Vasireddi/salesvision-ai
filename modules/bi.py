import plotly.graph_objects as go
from plotly.subplots import make_subplots

C = {
    'bg':'#0D0F1A','card':'#13162B','purple':'#6C63FF',
    'cyan':'#00D4FF','coral':'#FF6B6B','amber':'#FFD93D',
    'green':'#6BCB77','text':'#E8EAF6','muted':'#8892B0',
}

def render_bi_dashboard(bi_data):
    roi_results    = bi_data['roi_results']
    opt_records    = bi_data['opt_records']
    whatif_records = bi_data['whatif_records']

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=[
            'Channel ROI — Sales Lift per $1K',
            'Budget Optimizer — Optimal Allocation',
            'What-If Scenario Impact',
        ],
        horizontal_spacing=0.10,
    )

    # ── ROI bars ──
    channels  = list(roi_results.keys())
    roi_vals  = [roi_results[c]['roi_pct'] for c in channels]
    roi_colors = [C['green'] if v == max(roi_vals)
                  else C['amber'] if v > 0 else C['coral']
                  for v in roi_vals]

    fig.add_trace(go.Bar(
        x=channels, y=roi_vals,
        marker=dict(color=roi_colors, line=dict(color=C['bg'], width=1)),
        text=[f'{v:.1f}%' for v in roi_vals],
        textposition='outside',
        textfont=dict(color=C['text'], size=11),
        showlegend=False,
        hovertemplate='<b>%{x}</b><br>ROI: %{y:.2f}%<extra></extra>',
    ), row=1, col=1)

    # ── Stacked budget bars ──
    labels = [f'${r["total"]}K' for r in opt_records]
    for name, key, color in [
        ('TV',        'tv',        C['cyan']),
        ('Radio',     'radio',     C['amber']),
        ('Newspaper', 'newspaper', C['coral']),
    ]:
        fig.add_trace(go.Bar(
            name=name,
            x=labels,
            y=[r[key] for r in opt_records],
            marker=dict(color=color, opacity=0.85,
                        line=dict(color=C['bg'], width=0.5)),
            hovertemplate=f'<b>{name}</b>: ${{y:.1f}}K<extra></extra>',
        ), row=1, col=2)

    # ── What-if bars ──
    scenarios = [r['scenario'] for r in whatif_records]
    deltas    = [r['delta']    for r in whatif_records]

    fig.add_trace(go.Bar(
        x=deltas, y=scenarios,
        orientation='h',
        marker=dict(
            color=[C['green'] if d >= 0 else C['coral'] for d in deltas],
            opacity=0.85, line=dict(color=C['bg'], width=0.5)),
        text=[f'{d:+.3f}K' for d in deltas],
        textposition='outside',
        textfont=dict(color=C['text'], size=10),
        showlegend=False,
        hovertemplate='<b>%{y}</b><br>Change: %{x:+.3f}K<extra></extra>',
    ), row=1, col=3)

    fig.update_layout(
        paper_bgcolor=C['bg'], plot_bgcolor=C['card'],
        font=dict(color=C['text'], family='Inter, sans-serif', size=12),
        barmode='stack
