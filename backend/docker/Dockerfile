FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["gunicorn", "backend.app:app", "-b", "0.0.0.0:5000"]
