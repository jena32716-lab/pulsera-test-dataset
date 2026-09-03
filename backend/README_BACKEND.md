# Backend README

This backend provides a Flask REST API for PPG processing and simple rule-based detection.

Quickstart (local):

1. Create a virtualenv and install requirements:

   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt

2. Run the app:

   python backend/app.py

Endpoints:
- POST /predict : multipart/form-data with file field named 'file' (CSV) or JSON {signal: [...], time: [...]}.
- GET /health : health check

Notes: Models for advanced detectors are placeholders. Use backend/training to implement training.
