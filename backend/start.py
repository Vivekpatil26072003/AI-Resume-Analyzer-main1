#!/usr/bin/env python3
"""
Startup script for AI Resume Analyzer Backend
"""

import uvicorn
import os
import sys

def main():
    """Main function to start the FastAPI server"""
    
    # Add the current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"🚀 Starting AI Resume Analyzer Backend...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"📖 API Docs: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()




