import os
import sys
import subprocess
import time
import webbrowser
from threading import Thread

def run_backend():
    """Run the FastAPI backend server"""
    print("Iniciando el servidor backend...")
    os.chdir(os.path.join(os.path.dirname(__file__), "backend"))
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload"])

def run_frontend():
    """Run the Streamlit frontend"""
    print("Iniciando la aplicación frontend...")
    print("Ruta esperada:", os.path.join(os.path.dirname(__file__), "diet-planner", "frontend"))

    os.chdir(os.path.join(os.path.dirname(__file__), "frontend"))

    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

def open_browser():
    """Open browser after a delay to allow servers to start"""
    time.sleep(5)  # Wait for servers to start
    print("Abriendo la aplicación en el navegador...")
    webbrowser.open("http://localhost:8501")  # Streamlit default port

if __name__ == "__main__":
    # Check if required packages are installed
    try:
        import uvicorn
        import streamlit
        import fastapi
        import groq
    except ImportError:
        print("Instalando dependencias necesarias...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "streamlit", "groq"])
        print("Dependencias instaladas correctamente.")

    # Start backend in a separate thread
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Wait a moment for backend to initialize
    time.sleep(2)

    # Start browser in a separate thread
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Run frontend in the main thread
    run_frontend()
