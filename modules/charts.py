# ============================================================
# charts.py — Reusable Plotly chart functions
# ============================================================

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

C = {
    'bg': '#0D0F1A', 'card': '#13162B',
    'purple': '#6C63FF', 'cyan': '#00D4FF',
    'coral': '#FF6B6B', 'amber': '#FFD93D',
    'green': '#6BCB77', 'text': '#E8EAF6',
    'muted': '#8892B0', 'pink': '#FF6B9D',
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

def plot_scatter_regression(df):
    fig = make_subplots(rows=1, cols=3,
        subplot_titles=['TV vs Sales', 'Radio vs Sales',
                        'Newspaper vs Sales'],
        horizontal_spacing=0.1)
    channels = [('TV', C['cyan'], 1),
                ('Radio', C['amber'], 2),
                ('Newspaper', C['coral'], 3)]
    for ch, color, ci in channels:
        x = df[ch].values; y = df['Sales'].values
        r, _ = stats.pearsonr(x, y)
        slope, intercept, *_ = stats.linregress(x, y)
        x_line = np.linspace(x.min(), x.max(), 200)
        n    = len(x); se = np.sqrt(np.sum((y-(slope*x+intercept))**2)/(n-2))
        x_m  = x.mean()
        ci95 = 1.96*se*np.sqrt(1/n+(x_line-x_m)**2/np.sum((x-x_m)**2))
        fig.add_trace(go.Scatter(
            x=x, y=y, mode='markers',
            marker=dict(color=y, colorscale=[[0,C['coral']],[0.5,C['purple']],[1,C['cyan']]],
                        size=6, opacity=0.8, line=dict(color=C['bg'], width=0.4)),
            showlegend=False,
            hovertemplate=f'<b>{ch}:</b> %{{x:.1f}}<br><b>Sales:</b> %{{y:.1f}}<extra></extra>',
        ), row=1, col=ci)
        fig.add_trace(go.Scatter(
            x=x_line, y=slope*x_line+intercept,
            mode='lines', line=dict(color=C['text'], width=2),
            showlegend=False), row=1, col=ci)
        fig.add_trace(go.Scatter(
            x=np.concatenate([x_line, x_line[::-1]]),
            y=np.concatenate([slope*x_line+intercept+ci95,
                               (slope*x_line+intercept-ci95)[::-1]]),
            fill='toself', fillcolor='rgba(108,99,255,0.10)',
            line=dict(color='rgba(0,0,0,0)'),
            showlegend=False, hoverinfo='skip'), row=1, col=ci)
        fig.add_annotation(
            xref=f'x{ci if ci>1 else ""} domain',
            yref=f'y{ci if ci>1 else ""} domain',
            x=0.05, y=0.95,
            text=f'r = {r:.3f}', showarrow=False,
            font=dict(size=10, color=C['amber']),
            bgcolor=C['card'], borderpad=3, xanchor='left')
    theme(fig, h=380)
    for a in fig['layout']['annotations'][:3]:
        a['font'] = dict(color=C['muted'], size=11)
    return fig

def plot_correlation_heatmap(df):
    cols = df.columns.tolist(); n = len(cols)
    r_mat = np.zeros((n,n)); text = []
    for i,c1 in enumerate(cols):
        row = []
        for j,c2 in enumerate(cols):
            r, p = stats.pearsonr(df[c1], df[c2])
            r_mat[i,j] = round(r,3)
            sig = '***' if p<0.001 else ('**' if p<0.01 else ('*' if p<0.05 else ''))
            row.append(f'{r:.2f}{sig}' if i!=j else '1.00')
        text.append(row)
    fig = go.Figure(go.Heatmap(
        z=r_mat, x=cols, y=cols,
        text=text, texttemplate='%{text}',
        textfont=dict(size=12, color=C['text']),
        colorscale=[[0,C['coral']],[0.5,C['card']],[1,C['purple']]],
        zmid=0, zmin=-1, zmax=1,
        colorbar=dict(tickfont=dict(color=C['muted'])),
        hovertemplate='<b>%{x} × %{y}</b><br>r = %{z:.3f}<extra></extra>',
    ))
    theme(fig, h=380)
    fig.update_layout(
        yaxis=dict(autorange='reversed',
                   tickfont=dict(color=C['text'], size=12)),
        xaxis=dict(tickfont=dict(color=C['text'], size=12)),
    )
    return fig

def plot_distributions(df):
    fig = make_subplots(rows=1, cols=4,
        subplot_titles=['TV', 'Radio', 'Newspaper', 'Sales'],
        horizontal_spacing=0.08)
    configs = [('TV',C['cyan'],1), ('Radio',C['amber'],2),
               ('Newspaper',C['coral'],3), ('Sales',C['green'],4)]
    for col, color, ci in configs:
        data = df[col]; mu, sigma = data.mean(), data.std()
        fig.add_trace(go.Histogram(x=data, nbinsx=20,
            marker_color=color, opacity=0.7, showlegend=False,
            hovertemplate=f'{col}: %{{x:.1f}}<br>Count: %{{y}}<extra></extra>'),
            row=1, col=ci)
        x_r = np.linspace(data.min(), data.max(), 200)
        bw  = (data.max()-data.min())/20
        fig.add_trace(go.Scatter(x=x_r,
            y=stats.norm.pdf(x_r,mu,sigma)*len(data)*bw,
            mode='lines', line=dict(color=C['text'],width=1.5,dash='dot'),
            showlegend=False), row=1, col=ci)
        fig.add_vline(x=mu, line_dash='dash', line_color=C['amber'],
                      line_width=1.2, row=1, col=ci)
    theme(fig, h=340)
    for a in fig['layout']['annotations']:
        a['font'] = dict(color=C['muted'], size=11)
    return fig

def plot_3d_scatter(df):
    fig = go.Figure(go.Scatter3d(
        x=df['TV'], y=df['Radio'], z=df['Sales'],
        mode='markers',
        marker=dict(size=5, color=df['Sales'],
                    colorscale=[[0,C['coral']],[0.4,C['purple']],
                                [0.7,C['cyan']],[1,C['green']]],
                    opacity=0.85,
                    colorbar=dict(title='Sales',
                                  tickfont=dict(color=C['muted'])),
                    line=dict(color=C['bg'], width=0.3)),
        hovertemplate='TV: %{x:.1f}<br>Radio: %{y:.1f}<br>Sales: %{z:.1f}<extra></extra>',
    ))
    fig.update_layout(
        paper_bgcolor=C['bg'],
        scene=dict(bgcolor=C['card'],
                   xaxis=dict(title='TV', color=C['muted'],
                              gridcolor='#1E2340', showbackground=False),
                   yaxis=dict(title='Radio', color=C['muted'],
                              gridcolor='#1E2340', showbackground=False),
                   zaxis=dict(title='Sales', color=C['muted'],
                              gridcolor='#1E2340', showbackground=False),
                   camera=dict(eye=dict(x=1.5, y=1.5, z=1.1))),
        height=480, margin=dict(t=20,b=10,l=10,r=10),
        font=dict(color=C['text'], family='Inter'),
    )
    return fig

def plot_revenue_surface(df):
    X    = sm.add_constant(df[['TV','Radio']])
    mdl  = sm.OLS(df['Sales'], X).fit()
    coef = mdl.params
    tv_r = np.linspace(df['TV'].min(),    df['TV'].max(),    50)
    ra_r = np.linspace(df['Radio'].min(), df['Radio'].max(), 50)
    TV_g, Ra_g = np.meshgrid(tv_r, ra_r)
    Z = coef['const'] + coef['TV']*TV_g + coef['Radio']*Ra_g
    fig = go.Figure(go.Surface(
        x=tv_r, y=ra_r, z=Z,
        colorscale=[[0,C['coral']],[0.4,C['purple']],
                    [0.7,C['cyan']],[1,C['green']]],
        opacity=0.88,
        contours=dict(z=dict(show=True, usecolormap=True,
                             highlightcolor=C['amber'], project_z=True)),
        hovertemplate='TV: %{x:.1f}<br>Radio: %{y:.1f}<br>Pred Sales: %{z:.2f}<extra></extra>',
    ))
    fig.add_trace(go.Scatter3d(
        x=df['TV'], y=df['Radio'], z=df['Sales'],
        mode='markers', marker=dict(size=3, color=C['amber'], opacity=0.6),
        showlegend=False))
    fig.update_layout(
        paper_bgcolor=C['bg'],
        scene=dict(bgcolor=C['card'],
                   xaxis=dict(title='TV', color=C['muted'],
                              gridcolor='#1E2340', showbackground=False),
                   yaxis=dict(title='Radio', color=C['muted'],
                              gridcolor='#1E2340', showbackground=False),
                   zaxis=dict(title='Predicted Sales', color=C['muted'],
                              gridcolor='#1E2340', showbackground=False),
                   camera=dict(eye=dict(x=1.6, y=-1.6, z=1.2))),
        height=480, margin=dict(t=20,b=10,l=10,r=10),
        font=dict(color=C['text'], family='Inter'),
    )
    return fig
