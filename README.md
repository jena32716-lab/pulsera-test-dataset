# Root README

This repository contains a prototype scaffold for a PPG-based health issue detector.

Structure:
- backend/ : Flask API, preprocessing, feature extraction, training scaffolds
- frontend/: React app to upload CSVs and view predictions

I inspected the dataset under `test dataset/` and confirmed files like `sujeto1_PPG_INFO.csv` with columns: Tiempo, Senal_PPG, Edad, Sexo, Colesterol. The sampling interval looks ~0.0259s (approx 38.5 Hz). The backend loader is configured to read 'Senal_PPG' and 'Tiempo'.

Next steps I will take (after this commit):
- Implement training pipeline for per-issue supervised models if labels become available
- Improve detectors (train 1D-CNNs and RFs) and add model management endpoints
- Add unit tests and CI

To run locally: see backend/README_BACKEND.md and frontend README (not included yet)
