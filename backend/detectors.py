"""Simple rule-based and placeholder detectors.
These are starters: we implement brady/tachy rules and an irregularity (AF-like) heuristic.
Other detectors are placeholders that will be trained with labeled data.
"""

def run_detectors(features):
    if not features:
        return {'error':'no features extracted'}
    results = {}
    hr = features.get('hr_mean')

    # Bradycardia / Tachycardia
    results['brady'] = {'score': 1.0 if hr and hr < 50 else 0.0, 'label': int(hr is not None and hr < 50)}
    results['tachy'] = {'score': 1.0 if hr and hr > 100 else 0.0, 'label': int(hr is not None and hr > 100)}

    # HRV-based stress heuristic (low RMSSD -> lower vagal tone)
    rmssd = features.get('rmssd')
    if rmssd is None:
        results['stress'] = {'score': None, 'label': None, 'note':'insufficient data'}
    else:
        # normalize roughly (placeholder)
        score = max(0.0, min(1.0, (50.0 - rmssd) / 50.0))
        results['stress'] = {'score': score, 'label': int(score > 0.6)}

    # AF-like irregularity: high SDNN and high HR std
    sdnn = features.get('sdnn')
    hr_std = features.get('hr_std')
    irr_score = 0.0
    if sdnn is not None and hr_std is not None:
        irr_score = min(1.0, (sdnn / 0.2) * 0.5 + (hr_std / 10.0) * 0.5)
    results['arrhythmia_like'] = {'score': irr_score, 'label': int(irr_score > 0.6)}

    # Placeholders for other models (hypertension, sleep_apnea, general_anomaly)
    results['hypertension_risk'] = {'score': 0.0, 'note':'requires trained model'}
    results['sleep_apnea_like'] = {'score': 0.0, 'note':'requires trained model'}
    results['anomaly'] = {'score': 0.0, 'note':'requires trained model'}

    return results
