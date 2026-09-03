"""Preprocessing utilities for PPG signals."""
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt

def load_csv_from_file(fileobj):
    # fileobj: Werkzeug FileStorage or io.BytesIO
    s = fileobj.read().decode('utf-8')
    # Use pandas to read; header is expected on first line
    df = pd.read_csv(io.StringIO(s))
    # Accept known Spanish column names from dataset: 'Tiempo' and 'Senal_PPG'
    if 'Tiempo' not in df.columns:
        # try to fix if weird encoding
        df.columns = [c.strip() for c in df.columns]
    return df


def bandpass(signal, fs, low=0.5, high=8.0, order=3):
    nyq = 0.5 * fs
    lown = max(0.001, low / nyq)
    highn = min(0.999, high / nyq)
    b, a = butter(order, [lown, highn], btype='band')
    try:
        return filtfilt(b, a, signal)
    except Exception:
        # if filter fails (too few samples), return original
        return signal
