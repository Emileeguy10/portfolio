# Awesome Portfolio

A small Flask-based personal portfolio app.

Quick start

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
# or
python -m flask run
```

Notes
- Make sure `.env` contains `FLASK_APP=app.py` and `SECRET_KEY`.
- The app uses `python-dotenv` so environment variables from `.env` are loaded automatically.
