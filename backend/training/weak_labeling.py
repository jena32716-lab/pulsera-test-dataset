"""Create weak labels for the dataset using heuristics.
Outputs a CSV mapping each file to weak labels.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from processing.preprocess import bandpass
from processing.features import extract_time_features

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / 'test dataset'
OUT_PATH = REPO_ROOT / 'backend' / 'models' / 'weak_labels.csv'

THRESH_BRADY = 50.0
THRESH_TACHY = 100.0
THRESH_RMSSD_MS_STRESS = 25.0


def sleep_apnea_heuristic(df):
    # simple heuristic: count windows (60s) where mean amplitude drops >30% vs global median
    if 'Tiempo' not in df.columns:
        return 0
    t = df['Tiempo'].values
    sig = df['Senal_PPG'].values
    duration = t[-1] - t[0]
    if duration < 60*2:
        return 0
    # window size 60s
    wins = []
    start = t[0]
    med_amp = np.median(np.abs(sig - np.mean(sig)))
    while start < t[-1]:
        end = start + 60.0
        mask = (t >= start) & (t < end)
        if np.any(mask):
            wins.append(np.mean(np.abs(sig[mask] - np.mean(sig[mask]))))
        start = end
    if len(wins) == 0:
        return 0
    wins = np.array(wins)
    drops = np.sum(wins < 0.7 * med_amp)
    return int(drops >= 3)


def generate_labels_for_file(path):
    df = pd.read_csv(path)
    # ensure columns
    if 'Senal_PPG' not in df.columns:
        return None
    sig = df['Senal_PPG'].values
    # infer fs
    if 'Tiempo' in df.columns:
        dt = df['Tiempo'].diff().median()
        fs = int(round(1.0 / dt)) if dt and dt > 0 else 38
    else:
        fs = 38
    sigf = bandpass(sig, fs)
    feats = extract_time_features(sigf, fs)
    if not feats:
        return None
    hr_mean = feats.get('hr_mean')
    sdnn = feats.get('sdnn')
    rmssd = feats.get('rmssd')
    rmssd_ms = rmssd * 1000.0 if rmssd is not None else None

    brady = int(hr_mean is not None and hr_mean < THRESH_BRADY)
    tachy = int(hr_mean is not None and hr_mean > THRESH_TACHY)
    arrhythmia = int((sdnn is not None and sdnn > 0.12) or (feats.get('hr_std',0) > 8.0))
    stress = int(rmssd_ms is not None and rmssd_ms < THRESH_RMSSD_MS_STRESS)
    # hypertension proxy: age & cholesterol present in CSV
    htn = 0
    if 'Edad' in df.columns and 'Colesterol' in df.columns:
        try:
            age = float(df['Edad'].iloc[0])
            chol = float(df['Colesterol'].iloc[0])
            htn = int((age > 55 and chol > 240) or (chol > 300))
        except Exception:
            htn = 0

    sleep_apnea = sleep_apnea_heuristic(df)

    anomaly = 0
    if feats.get('n_peaks',0) < 10 or hr_mean is None or hr_mean < 30 or hr_mean > 200:
        anomaly = 1

    labels = {
        'file': path.name,
        'brady': brady,
        'tachy': tachy,
        'arrhythmia': arrhythmia,
        'stress': stress,
        'hypertension': htn,
        'sleep_apnea': sleep_apnea,
        'anomaly': anomaly
    }
    return labels


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in sorted(DATA_DIR.glob('*_PPG_INFO.csv')):
        try:
            lab = generate_labels_for_file(p)
            if lab:
                rows.append(lab)
                print('Labeled', p.name, lab)
            else:
                print('Skipped', p.name)
        except Exception as e:
            print('Error', p.name, e)
    if rows:
        dfout = pd.DataFrame(rows)
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        dfout.to_csv(OUT_PATH, index=False)
        print('Saved weak labels to', OUT_PATH)
    else:
        print('No labels generated')

if __name__ == '__main__':
    main()
