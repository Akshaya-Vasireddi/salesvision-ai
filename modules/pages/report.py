import streamlit as st
import numpy as np

def render(artifacts):
    df          = artifacts['df']
    best_name   = artifacts['best_name']
    all_results = artifacts['all_results']
    bi_data     = artifacts['bi_data']
    lb          = artifacts['leaderboard']
    from modules.bi import render_bi_dashboard

    r         = all_results[best_name]
    roi       = bi_data['roi_results']
    opt_200   = next(x for x in bi_data['opt_records'] if x['total']==200)
    whatif    = bi_data['whatif_records']
    best_roi  = max(roi, key=lambda x: roi[x]['roi_pct'])
    worst_roi = min(roi, key=lambda x: roi[x]['roi_pct'])

    tv_corr   = df['TV'].corr(df['Sales'])
    rad_corr  = df['Radio'].corr(df['Sales'])
    news_corr = df['Newspaper'].corr(df['Sales'])

    st.markdown("""
    <div class="page-header">
      <div class="page-title">📋 Executive Report</div>
      <div class="page-subtitle">
        Auto-generated business intelligence summary
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(render_bi_dashboard(bi_data),
                    use_container_width=True)

    st.markdown(f"""
    <div class="report-block">
      <div class="report-title">📊 Dataset Overview</div>
      Analysed <b>{len(df)} advertising campaigns</b> across three channels:
      TV, Radio, and Newspaper. Average total spend per campaign:
      <b>${df['TV'].mean()+df['Radio'].mean()+df['Newspaper'].mean():.1f}K</b>.
      Average sales revenue: <b>${df['Sales'].mean():.2f}K</b>
      (range: ${df['Sales'].min():.1f}K — ${df['Sales'].max():.1f}K).
    </div>

    <div class="report-block">
      <div class="report-title">🔗 Channel Effectiveness</div>
      <b>TV</b> is the strongest revenue driver
      (Pearson r = {tv_corr:.3f}, explains {tv_corr**2*100:.1f}% of
      sales variance). <b>Radio</b> is a meaningful secondary channel
      (r = {rad_corr:.3f}). <b>Newspaper</b> shows the weakest signal
      (r = {news_corr:.3f}, explains only {news_corr**2*100:.1f}% of
      variance) and is the primary candidate for reallocation.
    </div>

    <div class="report-block">
      <div class="report-title">🤖 Model Performance</div>
      Best model: <b>{best_name}</b>.<br>
      Validation R² = {r['val_r2']:.4f} |
      Test R² = {r['test_r2']:.4f} |
      RMSE = ±{r['test_rmse']:.2f}K.<br>
      The model predicts within ±{r['test_rmse']:.2f}K of actual sales —
      suitable for budget planning decisions.
      {len(lb)} models were benchmarked;
      {best_name} ranked #1 on validation R².
    </div>

    <div class="report-block">
      <div class="report-title">💡 ROI Analysis</div>
      <b>{best_roi}</b> delivers the highest marginal ROI:
      {roi[best_roi]['roi_pct']:.1f}% sales lift per $1K incremental spend.<br>
      <b>{worst_roi}</b> delivers the weakest return:
      {roi[worst_roi]['roi_pct']:.1f}% — primary reallocation candidate.<br>
      Shifting 50% of Newspaper budget to Radio is estimated to yield
      +{next(w['delta'] for w in whatif if 'News → Radio' in w['scenario']):.3f}K
      in sales.
    </div>

    <div class="report-block">
      <div class="report-title">🎯 Recommendations</div>
      1. <b>Prioritise {best_roi} spend</b> — highest return on
         incremental investment.<br>
      2. <b>Review Newspaper allocation</b> — weakest ROI,
         consider partial reallocation to TV or Radio.<br>
      3. <b>At $200K total budget</b>, optimal allocation is:
         TV ${opt_200['tv']:.0f}K /
         Radio ${opt_200['radio']:.0f}K /
         Newspaper ${opt_200['newspaper']:.0f}K
         (expected sales: ${opt_200['predicted_sales']:.2f}K).<br>
      4. <b>Use the What-If Simulator</b> to model specific
         budget scenarios before committing spend.
    </div>
    """, unsafe_allow_html=True)
