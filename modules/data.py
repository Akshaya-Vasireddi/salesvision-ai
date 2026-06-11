import pandas as pd
import numpy as np
import pickle
import os

# Get the data folder relative to this file
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'data')

def load_all_artifacts():
    df     = pd.read_csv(os.path.join(DATA, 'advertising_clean.csv'))
    df_eng = pd.read_csv(os.path.join(DATA, 'advertising_engineered.csv'))

    X_train    = pd.read_csv(os.path.join(DATA, 'X_train.csv'))
    X_val      = pd.read_csv(os.path.join(DATA, 'X_val.csv'))
    X_test     = pd.read_csv(os.path.join(DATA, 'X_test.csv'))
    X_train_sc = pd.read_csv(os.path.join(DATA, 'X_train_sc.csv'))
    X_val_sc   = pd.read_csv(os.path.join(DATA, 'X_val_sc.csv'))
    X_test_sc  = pd.read_csv(os.path.join(DATA, 'X_test_sc.csv'))
    y_train    = pd.read_csv(os.path.join(DATA, 'y_train.csv')).squeeze()
    y_val      = pd.read_csv(os.path.join(DATA, 'y_val.csv')).squeeze()
    y_test     = pd.read_csv(os.path.join(DATA, 'y_test.csv')).squeeze()

    with open(os.path.join(DATA, 'all_models.pkl'),     'rb') as f: all_results    = pickle.load(f)
    with open(os.path.join(DATA, 'best_model.pkl'),     'rb') as f: best_data      = pickle.load(f)
    with open(os.path.join(DATA, 'scaler.pkl'),         'rb') as f: scaler         = pickle.load(f)
    with open(os.path.join(DATA, 'final_features.pkl'), 'rb') as f: final_features = pickle.load(f)
    with open(os.path.join(DATA, 'shap_artifacts.pkl'), 'rb') as f: shap_raw       = pickle.load(f)
    with open(os.path.join(DATA, 'bi_artifacts.pkl'),   'rb') as f: bi_raw         = pickle.load(f)

    best_name  = best_data['name']
    best_info  = best_data['info']
    best_model = best_info['model']
    is_scaled  = best_info['scaled']

    shap_data = {
        'shap_train':    shap_raw['shap_train'],
        'shap_val':      shap_raw['shap_val'],
        'expected_val':  float(shap_raw['expected_val']),
        'importance_df': shap_raw['importance_df'],
    }

    bi_data = {
        'roi_results':    bi_raw['roi_results'],
        'opt_records':    bi_raw['opt_records'],
        'whatif_records': bi_raw['whatif_records'],
    }

    leaderboard = pd.read_csv(os.path.join(DATA, 'leaderboard.csv'))

    X_tr_shap = X_train_sc if is_scaled else X_train
    X_vl_shap = X_val_sc   if is_scaled else X_val

    return {
        'df': df, 'df_eng': df_eng,
        'X_train': X_train, 'X_val': X_val, 'X_test': X_test,
        'X_train_sc': X_train_sc, 'X_val_sc': X_val_sc, 'X_test_sc': X_test_sc,
        'y_train': y_train, 'y_val': y_val, 'y_test': y_test,
        'X_tr_shap': X_tr_shap, 'X_vl_shap': X_vl_shap,
        'all_results': all_results, 'best_name': best_name,
        'best_model': best_model, 'best_info': best_info,
        'is_scaled': is_scaled, 'scaler': scaler,
        'final_features': final_features, 'leaderboard': leaderboard,
        'shap_data': shap_data, 'bi_data': bi_data,
    }
