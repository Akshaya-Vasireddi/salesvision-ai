# ============================================================
# explain.py — SHAP visualizations for Streamlit
# ============================================================

import plotly.graph_objects as go
import numpy as np

C = {
    'bg': '#0D0F1A', 'card': '#13162B',
    'purple': '#6C63FF', 'cyan': '#00D4FF',
    'coral': '#FF6B6B', 'amber': '#FFD93D',
    'green': '#6BCB77', 'text': '#E8EAF6',
    'muted': '#8892B0',
}

def theme(fig, title='', h=420):
    fig.update_layout(
        paper_bgcolor=C['bg'], plot_bgcolor=C['card'],
        font=dict(color=C['text'], family='Inter, sans-serif', size=12),
        title=dict(text=title, font=dict(size=17, color=C['text']),
                   x=0.5, xanchor='center', y=0.97),
        xaxis=dict(gridcolor='#1E2340', zeroline=False,
                   tickfont=dict(color=C['muted'])),
        yaxis=dict(gridcolor='#1E2340', zeroline=False,
                   tickfont=dict(color=C['muted'])),
        hoverlabel=dict(bgcolor=C['card'], font_color=C['text'],
                        bordercolor=C['purple']),
        margin=dict(t=70, b=55, l=60, r=30),
        height=h,
    )
    return fig

def plot_global_importance(shap_data, X_tr_shap):
    shap_arr  = np.array(shap_data['shap_train'])
    mean_shap = np.abs(shap_arr).mean(axis=0)
    feats     = list(X_tr_shap.columns)
    imp_df    = sorted(zip(feats, mean_shap), key=lambda x: x[1])
    names     = [x[0] for x in imp_df]
    vals      = [x[1] for x in imp_df]
    total     = sum(vals)
    colors    = [C['green'] if v >= np.quantile(vals, 0.75)
                 else C['cyan']  if v >= np.quantile(vals, 0.50)
                 else C['amber'] if v >= np.quantile(vals, 0.25)
                 else C['coral'] for v in vals]
    fig = go.Figure(go.Bar(
        x=vals, y=names, orientation='h',
        marker=dict(color=colors, line=dict(color=C['bg'], width=0.5)),
        text=[f'{v:.3f} ({v/total*100:.1f}%)' for v in vals],
        textposition='outside',
        textfont=dict(color=C['muted'], size=9),
        hovertemplate='<b>%{y}</b><br>Mean |SHAP|: %{x:.4f}<extra></extra>',
    ))
    theme(fig, '🎯 Global Feature Importance — Mean |SHAP|',
          h=max(360, len(names)*34))
    fig.update_layout(
        xaxis=dict(title='Mean |SHAP| value'),
        bargap=0.28,
    )
    return fig

def plot_waterfall_chart(shap_data, X_vl_shap, y_val):
    shap_arr    = np.array(shap_data['shap_val'])
    expected    = float(shap_data['expected_val'])
    median_idx  = int(np.abs(y_val.values - y_val.median()).argmin())
    sv          = shap_arr[median_idx]
    feat_names  = list(X_vl_shap.columns)
    feat_values = X_vl_shap.iloc[median_idx].values
    order       = np.argsort(np.abs(sv))
    sv_ord      = sv[order]
    fn_ord      = [feat_names[i] for i in order]
    fv_ord      = feat_values[order]
    cumulative  = np.concatenate([[expected],
                                   expected + np.cumsum(sv_ord)])
    prediction  = expected + sv.sum()
    colors      = [C['green'] if v >= 0 else C['coral'] for v in sv_ord]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Baseline'], y=[expected],
        marker=dict(color=C['muted'], opacity=0.6),
        showlegend=False,
        hovertemplate=f'Baseline: ${expected:.2f}K<extra></extra>',
    ))
    for i, (feat, val, fv, color) in enumerate(
            zip(fn_ord, sv_ord, fv_ord, colors)):
        fig.add_trace(go.Bar(
            x=[feat], y=[abs(val)],
            base=[cumulative[i] if val >= 0 else cumulative[i]+val],
            marker=dict(color=color, opacity=0.85,
                        line=dict(color=C['bg'], width=0.5)),
            showlegend=False,
            text=f'{val:+.2f}',
            textposition='outside',
            textfont=dict(color=C['green'] if val>=0 else C['coral'], size=9),
            hovertemplate=f'<b>{feat}</b>: {fv:.2f}<br>SHAP: {val:+.3f}K<extra></extra>',
        ))
    fig.add_trace(go.Bar(
        x=['Prediction'], y=[prediction],
        marker=dict(color=C['purple'], opacity=0.9,
                    line=dict(color=C['cyan'], width=2)),
        showlegend=False,
        text=f'${prediction:.2f}K',
        textposition='outside',
        textfont=dict(color=C['cyan'], size=11),
        hovertemplate=f'Prediction: ${prediction:.2f}K<extra></extra>',
    ))
    theme(fig, '🔍 Waterfall — Prediction Breakdown', h=440)
    fig.update_layout(
        yaxis=dict(title='Sales ($K)'), bargap=0.3)
    return fig, round(prediction, 2), round(y_val.iloc[median_idx], 2)

def plot_beeswarm(shap_data, X_tr_shap):
    shap_arr   = np.array(shap_data['shap_train'])
    feat_names = list(X_tr_shap.columns)
    order      = np.argsort(np.abs(shap_arr).mean(axis=0))
    fig        = go.Figure()
    for rank, feat_idx in enumerate(order):
        feat    = feat_names[feat_idx]
        sv      = shap_arr[:, feat_idx]
        fv      = X_tr_shap.iloc[:, feat_idx].values
        fv_norm = (fv - fv.min()) / (fv.max() - fv.min() + 1e-9)
        np.random.seed(int(feat_idx))
        jitter  = np.random.uniform(-0.22, 0.22, len(sv))
        is_last = bool(feat_idx == order[-1])
        fig.add_trace(go.Scatter(
            x=sv, y=np.full(len(sv), rank) + jitter,
            mode='markers',
            marker=dict(
                color=fv_norm,
                colorscale=[[0,'#4575b4'],[0.5,C['card']],[1,C['coral']]],
                size=4, opacity=0.7,
                colorbar=dict(
                    title=dict(text='Feature value',
                               font=dict(color=C['muted'],size=9)),
                    tickvals=[0,1], ticktext=['Low','High'],
                    tickfont=dict(color=C['muted'],size=8),
                    len=0.35, y=0.5, x=1.01, thickness=10,
                ) if is_last else None,
                showscale=is_last,
            ),
            name=feat, showlegend=False,
            hovertemplate=f'<b>{feat}</b><br>SHAP: %{{x:.3f}}<extra></extra>',
        ))
    fig.update_layout(
        yaxis=dict(tickmode='array',
                   tickvals=list(range(len(feat_names))),
                   ticktext=[feat_names[i] for i in order],
                   tickfont=dict(color=C['text'], size=10)),
    )
    theme(fig, '🐝 SHAP Beeswarm — Impact Distribution', h=480)
    fig.add_vline(x=0, line_dash='dash',
                  line_color=C['muted'], line_width=1)
    fig.update_layout(
        xaxis=dict(title='SHAP value (impact on prediction $K)'))
    return fig
