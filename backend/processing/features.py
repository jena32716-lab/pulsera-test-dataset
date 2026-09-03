"""Feature extraction for PPG signals."""
import numpy as np
from scipy.signal import find_peaks

def detect_peaks(ppg_signal, fs, distance_sec=0.4):
    distance = int(max(1, distance_sec * fs))
    peaks, props = find_peaks(ppg_signal, distance=distance)
    return peaks

def extract_time_features(ppg_signal, fs):
    peaks = detect_peaks(ppg_signal, fs)
    if len(peaks) < 2:
        return {}
    rr = np.diff(peaks) / float(fs)  # seconds
    hr = 60.0 / rr
    feats = {
        'n_peaks': int(len(peaks)),
        'mean_rr': float(np.mean(rr)),
        'sdnn': float(np.std(rr, ddof=1)),
        'rmssd': float(np.sqrt(np.mean(np.diff(rr)**2))),
        'hr_mean': float(np.mean(hr)),
        'hr_std': float(np.std(hr)),
    }
    return feats
