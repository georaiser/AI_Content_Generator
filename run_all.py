# run_all.py
import subprocess
import os

backend = subprocess.Popen(["uvicorn", "backend.src.server:app", "--reload", "--port", "8000"])

frontend = subprocess.Popen([
    "streamlit", "run", "frontend/src/ui.py",
    "--server.port", "8502"
], env={**os.environ, "PYTHONPATH": os.getcwd(), "API_URL": "http://localhost:8000/content_generator"})

backend.wait()
frontend.wait()
