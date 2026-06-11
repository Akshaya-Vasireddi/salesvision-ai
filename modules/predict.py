# ============================================================
# predict.py — Prediction, optimizer, what-if engine
# ============================================================

import pandas as pd
import numpy as np
from scipy.optimize import minimize

def build_feature_row(tv, radio, newspaper, final_features):
    total = tv + radio + newspaper + 1e-9
    row = {
        'TV':               tv,
        'Radio':            radio,
        'Newspaper':        newspaper,
        'TV_Radio':         tv * radio,
        'TV_Newspaper':     tv * newspaper,
        'Radio_Newspaper':  radio * newspaper,
        'Total_Budget':     total,
        'TV_Ratio':         tv    / total,
        'Radio_Ratio':      radio / total,
        'Newspaper_Ratio':  newspaper / total,
        'Mass_Reach':       tv + radio,
        'Log_TV':           np.log1p(tv),
        'Log_Radio':        np.log1p(radio),
        'Log_Newspaper':    np.log1p(newspaper),
        'TV_sq':            tv ** 2,
        'Radio_sq':         radio ** 2,
    }
    return pd.DataFrame([row])[final_features]

def make_prediction(tv, radio, newspaper, artifacts):
    model  = artifacts['best_model']
    feats  = artifacts['final_features']
    scaler = artifacts['scaler']
    scaled = artifacts['is_scaled']

    X = build_feature_row(tv, radio, newspaper, feats)
    if scaled:
        X = pd.DataFrame(scaler.transform(X), columns=feats)

    pred = float(model.predict(X)[0])

    # Bootstrap CI (50 samples for speed)
    Xtr = artifacts['X_tr_shap']
    ytr = artifacts['y_train']
    preds_boot = []
    for _ in range(50):
        idx  = np.random.choice(len(Xtr), len(Xtr), replace=True)
        Xb   = Xtr.iloc[idx]
        yb   = ytr.iloc[idx]
        m    = type(model)(**model.get_params())
        m.fit(Xb, yb)
        Xi   = build_feature_row(tv, radio, newspaper, feats)
        if scaled:
            Xi = pd.DataFrame(scaler.transform(Xi), columns=feats)
        preds_boot.append(float(m.predict(Xi)[0]))

    lower = np.percentile(preds_boot, 2.5)
    upper = np.percentile(preds_boot, 97.5)

    return {
        'prediction': round(pred, 2),
        'lower_ci':   round(lower, 2),
        'upper_ci':   round(upper, 2),
        'confidence': round((1 - abs(pred - np.mean(preds_boot))
                             / (pred + 1e-9)) * 100, 1),
    }

def run_budget_optimizer(total_budget, artifacts):
    model  = artifacts['best_model']
    feats  = artifacts['final_features']
    scaler = artifacts['scaler']
    scaled = artifacts['is_scaled']

    def neg_sales(x):
        tv, radio = x[0], x[1]
        newspaper = total_budget - tv - radio
        if newspaper < 0 or tv < 0 or radio < 0:
            return 999.0
        X = build_feature_row(tv, radio, newspaper, feats)
        if scaled:
            X = pd.DataFrame(scaler.transform(X), columns=feats)
        return -float(model.predict(X)[0])

    bounds = [(0, total_budget), (0, total_budget)]
    cons   = [{'type': 'ineq',
               'fun': lambda x, t=total_budget: t - x[0] - x[1]}]
    best_result = None
    best_val    = 999.0

    # Multi-start optimization
    for tv_start in [0.3, 0.5, 0.7, 0.8]:
        for rad_start in [0.1, 0.2, 0.3]:
            x0 = [total_budget * tv_start,
                  total_budget * rad_start]
            r  = minimize(neg_sales, x0, method='SLSQP',
                          bounds=bounds, constraints=cons,
                          options={'ftol': 1e-8, 'maxiter': 300})
            if r.fun < best_val:
                best_val    = r.fun
                best_result = r

    tv_opt    = max(0.0, round(float(best_result.x[0]), 1))
    radio_opt = max(0.0, round(float(best_result.x[1]), 1))
    news_opt  = max(0.0, round(total_budget - tv_opt - radio_opt, 1))
    pred_opt  = round(-float(best_result.fun), 2)

    return {
        'tv':        tv_opt,
        'radio':     radio_opt,
        'newspaper': news_opt,
        'predicted': pred_opt,
        'tv_pct':    round(tv_opt    / total_budget * 100, 1),
        'radio_pct': round(radio_opt / total_budget * 100, 1),
        'news_pct':  round(news_opt  / total_budget * 100, 1),
    }

def run_whatif(base_tv, base_radio, base_newspaper,
               tv_delta_pct, radio_delta_pct, news_delta_pct,
               artifacts):
    model  = artifacts['best_model']
    feats  = artifacts['final_features']
    scaler = artifacts['scaler']
    scaled = artifacts['is_scaled']

    def predict(tv, radio, newspaper):
        X = build_feature_row(tv, radio, newspaper, feats)
        if scaled:
            X = pd.DataFrame(scaler.transform(X), columns=feats)
        return float(model.predict(X)[0])

    base_sales = predict(base_tv, base_radio, base_newspaper)
    new_tv     = base_tv    * (1 + tv_delta_pct    / 100)
    new_radio  = base_radio * (1 + radio_delta_pct / 100)
    new_news   = base_newspaper * (1 + news_delta_pct / 100)
    new_sales  = predict(new_tv, new_radio, new_news)

    return {
        'base_sales':  round(base_sales, 2),
        'new_sales':   round(new_sales,  2),
        'delta':       round(new_sales - base_sales, 3),
        'pct_change':  round((new_sales - base_sales) / base_sales * 100, 1),
        'new_tv':      round(new_tv,    1),
        'new_radio':   round(new_radio, 1),
        'new_news':    round(new_news,  1),
    }
