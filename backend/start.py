#!/usr/bin/env python3
"""Local startup script for the existing Flask backend."""

import os

from app.main import app


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes", "on"}
    reload = os.getenv("RELOAD", "false").lower() in {"1", "true", "yes", "on"}

    print("Starting AI Resume Analyzer Backend...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"Health Check: http://{host}:{port}/health")

    app.run(host=host, port=port, debug=debug, use_reloader=reload)

if __name__ == "__main__":
    main()




