# Loan Predictor

A small Flask + JavaScript demo that predicts simple loan eligibility using a Decision Tree model. The repository includes a web UI (index.html + script.js), a Flask API (app.py) that serves predictions, and a training script (train_model.py) that produces `loan_model.pkl`.

This project is intended as a minimal demo and learning example — not production-ready financial advice.

## Features
- Simple web UI to enter applicant details and get an eligibility result.
- Flask API endpoint: POST /predict
- Model training script to generate a pickled scikit-learn model.
- Guidance for deploying to Render (requirements, Procfile, Dockerfile included in the repo examples).

## Quick demo
1. Open `index.html` in your browser (or run the Flask app and visit the rendered site).
2. Fill in details and click "Check Eligibility".
3. The frontend calls `POST /predict` to return "Eligible ✅" or "Not Eligible ❌".

## Repository structure (important files)
- app.py — Flask application that loads `loan_model.pkl` and exposes `/predict`.
- index.html, script.js, style.css — frontend UI.
- train_model.py — script to generate `loan_model.pkl` (uses scikit-learn).
- loan_model.pkl — pre-trained model (if included).
- requirements.txt, Procfile, Dockerfile, render.yaml — deployment helpers (may be examples / not present by default).

## Requirements
- Python 3.8+ (use the same Python version you used to create `loan_model.pkl` if possible)
- Recommended: create a virtual environment
- Pin package versions. Best practice: on your dev machine run:
```bash
pip freeze > requirements.txt
```
and commit `requirements.txt`.

Typical packages (example; replace with the exact versions from your environment):
```
Flask==2.2.5
flask-cors==3.0.10
numpy==1.24.3
scikit-learn==1.2.2
joblib==1.2.0
gunicorn==20.1.0
```

## Run locally (development)
1. Clone the repo
```bash
git clone https://github.com/PARESH671/loan-predictor.git
cd loan-predictor
```
2. Create and activate a virtual environment
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```
3. Install dependencies
```bash
pip install --upgrade pip
# If you have requirements.txt:
pip install -r requirements.txt
```
4. If `loan_model.pkl` is not present or you want to regenerate it:
```bash
python train_model.py
# This will create loan_model.pkl in the repo root
```
5. Run the Flask app (development)
```bash
# Development mode (Flask builtin server)
python app.py
# OR recommended production-style server
gunicorn app:app --bind 0.0.0.0:5000
```
6. Open the frontend:
- If running app locally, open `index.html` in the browser (the frontend currently posts to http://127.0.0.1:5000/predict).
- If you host frontend and backend together, ensure the frontend points to the correct host/port or use relative paths.

Notes: app.py uses PORT env var and binds to 0.0.0.0 for deployment compatibility (Render/containers).

## API
POST /predict
- Content-Type: application/json
- Request body:
```json
{
  "income": 50000,
  "age": 30,
  "credit_score": 720,
  "loan_amount": 10000
}
```
- Response:
```json
{"status":"Eligible ✅"}
# or
{"status":"Not Eligible ❌"}
```

On error, API returns JSON with `error` and HTTP status 400.

## Deployment to Render (tips)
There are two recommended approaches:

1. Native Python (Procfile)
- Commit `requirements.txt` and `Procfile`:
  - Procfile: `web: gunicorn app:app --bind 0.0.0.0:$PORT`
- In Render service settings, select Python environment and use default build command `pip install -r requirements.txt`.
- Important: Pin exact package versions in `requirements.txt` to avoid Render installing incompatible versions (especially scikit-learn/joblib mismatches that break loading pickled models).

2. Docker (recommended)
- Add `Dockerfile` to lock Python version and packages.
- Build locally or let Render build from Dockerfile — ensures reproducible runtime and avoids silent downgrades.
- Example build/run:
```bash
docker build -t loan-predictor .
docker run -p 5000:5000 loan-predictor
```

Common Render issues
- Model load errors such as pickle protocol errors or incompatible scikit-learn/joblib versions:
  - Fix: pin package versions in `requirements.txt` to match the environment where `loan_model.pkl` was created; or retrain the model on the server during build (e.g., run `python train_model.py` in Dockerfile or buildCommand).
- Ensure the app reads and uses the PORT env var and binds to 0.0.0.0.

## Troubleshooting
- If `joblib.load('loan_model.pkl')` fails:
  - Check logs for scikit-learn / joblib version mismatch message.
  - Recreate `loan_model.pkl` with the same scikit-learn version you intend to use in production.
  - Optionally, retrain at build time (safer if you cannot determine exact package versions).
- If frontend shows "Backend Offline" or cannot fetch:
  - Ensure the frontend's fetch URL matches the backend host/port (use relative paths in production).
  - CORS: app.py enables CORS via `flask_cors.CORS(app)`.

## Contributing
- Suggestions, bug reports, and PRs welcome.
- Before submitting PRs, run linters/tests (if added) and ensure the app runs locally.
- If adding dependencies, update `requirements.txt` via `pip freeze > requirements.txt`.

## License
This repo does not include an explicit license. Add a LICENSE file if you want to make the project open-source with a specific license (e.g., MIT).

## Contact
Author: PARESH671 (GitHub)
- Repo: https://github.com/PARESH671/loan-predictor

If you want, I can:
- Commit this README to the repo and open a PR, or
- Also create a more deployment-focused README section with exact Render steps and example `render.yaml`.

```
