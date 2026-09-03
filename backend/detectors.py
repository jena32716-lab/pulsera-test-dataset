"""Updated detectors to use trained models if available, else fallback to heuristics."""
import joblib
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent / 'models'

# Try to load models for tasks
MODEL_TASKS = ['brady', 'tachy', 'arrhythmia', 'stress', 'hypertension', 'sleep_apnea', 'anomaly']
MODELS = {}
for t in MODEL_TASKS:
    p = MODELS_DIR / f'{t}.joblib'
    if p.exists():
        try:
            MODELS[t] = joblib.load(p)
        except Exception:
            MODELS[t] = None
    else:
        MODELS[t] = None


def predict_with_models(features):
    # features: dict name->value
    if not features:
        return None
    X = [features.get(k, 0) for k in ['n_peaks','mean_rr','sdnn','rmssd','hr_mean','hr_std']]
    res = {}
    for t, model in MODELS.items():
        if model is None:
            res[t] = None
        else:
            try:
                pred_proba = model.predict_proba([X])[0]
                score = float(pred_proba[1]) if len(pred_proba)>1 else float(pred_proba[0])
                res[t] = {'score': score, 'label': int(score>0.5)}
            except Exception:
                try:
                    pred = model.predict([X])[0]
                    res[t] = {'score': float(pred), 'label': int(pred)}
                except Exception:
                    res[t] = None
    return res


def run_detectors(features):
    # If trained models available, use them
    model_preds = predict_with_models(features)
    results = {}
    if model_preds:
        # merge model outputs with heuristics for any missing
        for k,v in model_preds.items():
            if v is not None:
                results[k] = v
    # fallback heuristics for missing tasks
    hr = features.get('hr_mean')
    if 'brady' not in results:
        results['brady'] = {'score': 1.0 if hr and hr < 50 else 0.0, 'label': int(hr is not None and hr < 50)}
    if 'tachy' not in results:
        results['tachy'] = {'score': 1.0 if hr and hr > 100 else 0.0, 'label': int(hr is not None and hr > 100)}
    if 'stress' not in results:
        rmssd = features.get('rmssd')
        if rmssd is None:
            results['stress'] = {'score': None, 'label': None, 'note':'insufficient data'}
        else:
            score = max(0.0, min(1.0, (50.0 - rmssd*1000.0) / 50.0))
            results['stress'] = {'score': score, 'label': int(score > 0.6)}
    if 'arrhythmia' not in results:
        sdnn = features.get('sdnn')
        hr_std = features.get('hr_std')
        irr_score = 0.0
        if sdnn is not None and hr_std is not None:
            irr_score = min(1.0, (sdnn / 0.2) * 0.5 + (hr_std / 10.0) * 0.5)
        results['arrhythmia'] = {'score': irr_score, 'label': int(irr_score > 0.6)}
    # placeholders for others
    for t in ['hypertension','sleep_apnea','anomaly']:
        if t not in results:
            results[t] = {'score': 0.0, 'note':'no model; heuristic not implemented'}
    return results
