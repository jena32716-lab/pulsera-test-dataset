from flask import Flask, request, jsonify
import io
import pandas as pd
from processing.preprocess import load_csv_from_file, bandpass
from processing.features import extract_time_features
from detectors import run_detectors

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/predict', methods=['POST'])
def predict():
    # Accept file upload or JSON with signal
    if 'file' in request.files:
        f = request.files['file']
        df = load_csv_from_file(f)
    else:
        data = request.get_json() or {}
        signal = data.get('signal')
        times = data.get('time')
        if signal is None:
            return jsonify({'error':'no file or signal provided'}), 400
        df = pd.DataFrame({'Tiempo': times if times is not None else list(range(len(signal))), 'Senal_PPG': signal})

    # infer sampling rate
    fs = max(1, int(round(1.0 / df['Tiempo'].diff().median())))

    sig = df['Senal_PPG'].values
    sigf = bandpass(sig, fs)
    feats = extract_time_features(sigf, fs)

    results = run_detectors(feats)
    return jsonify({'features': feats, 'results': results, 'fs': fs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
