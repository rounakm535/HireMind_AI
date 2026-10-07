#!/usr/bin/env python3
"""
HireMind AI - Local Development Launcher
Concurrently starts FastAPI Backend (port 8000) and Vite React Frontend (port 5173).
"""

import os
import sys
import subprocess
import time
import signal

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")

    print("=" * 60)
    print("🚀 Launching HireMind AI - Applicant Tracking System")
    print("=" * 60)
    print(f"📁 Workspace Root: {root_dir}")
    print("⚙️  Starting FastAPI Backend on http://localhost:8000 ...")
    print("⚙️  Starting React Frontend on http://localhost:5173 ...")
    print("=" * 60)

    # Determine Python executable
    python_exe = sys.executable

    # Command to run backend
    backend_cmd = [
        python_exe, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000", "--host", "127.0.0.1"
    ]

    # Command to run frontend (using npx vite or npm run dev)
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_cmd = [npm_cmd, "run", "dev"]

    processes = []

    try:
        # Start Backend
        backend_proc = subprocess.Popen(backend_cmd, cwd=backend_dir)
        processes.append(("Backend (FastAPI)", backend_proc))

        # Start Frontend
        frontend_proc = subprocess.Popen(frontend_cmd, cwd=frontend_dir)
        processes.append(("Frontend (Vite)", frontend_proc))

        print("\n✅ Systems active!")
        print("🔗 Open http://localhost:5173 in your browser to access the app.\n")
        print("Press Ctrl+C to stop all servers.\n")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers gracefully...")
        for name, proc in processes:
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except Exception:
                proc.kill()
        print("✨ Done.")

if __name__ == "__main__":
    main()
