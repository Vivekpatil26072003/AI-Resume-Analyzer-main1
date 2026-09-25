#!/usr/bin/env python3
"""
Setup script for AI Resume Analyzer
This script automates the setup process for both backend and frontend
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Exception running command: {command}")
        print(f"Error: {str(e)}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} detected")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js is not installed. Please install Node.js 16 or higher")
    return False

def setup_backend():
    """Setup the FastAPI backend"""
    print("\n🔧 Setting up Backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Create virtual environment
    print("📦 Creating virtual environment...")
    if not run_command("python -m venv venv", cwd=backend_dir):
        return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    print("📦 Installing Python dependencies...")
    if not run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir):
        return False
    
    # Download spaCy model
    print("🤖 Downloading spaCy model...")
    if not run_command(f"{pip_cmd} install spacy", cwd=backend_dir):
        return False
    
    if not run_command(f"{pip_cmd} -m spacy download en_core_web_sm", cwd=backend_dir):
        print("⚠️  Warning: Could not download spaCy model. You may need to install it manually.")
    
    print("✅ Backend setup completed!")
    return True

def setup_frontend():
    """Setup the Next.js frontend"""
    print("\n🔧 Setting up Frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install Node.js dependencies
    print("📦 Installing Node.js dependencies...")
    if not run_command("npm install", cwd=frontend_dir):
        return False
    
    print("✅ Frontend setup completed!")
    return True

def create_env_files():
    """Create environment files from examples"""
    print("\n📝 Creating environment files...")
    
    # Backend env file
    backend_env_example = Path("backend/env.example")
    backend_env = Path("backend/.env")
    
    if backend_env_example.exists() and not backend_env.exists():
        backend_env_example.copy(backend_env)
        print("✅ Created backend/.env file")
    
    # Frontend env file
    frontend_env_example = Path("frontend/env.local.example")
    frontend_env = Path("frontend/.env.local")
    
    if frontend_env_example.exists() and not frontend_env.exists():
        frontend_env_example.copy(frontend_env)
        print("✅ Created frontend/.env.local file")

def main():
    """Main setup function"""
    print("🚀 AI Resume Analyzer Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not check_node_version():
        return
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        return
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed")
        return
    
    # Create environment files
    create_env_files()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the backend server:")
    print("   cd backend")
    print("   python start.py")
    print("\n2. Start the frontend server (in a new terminal):")
    print("   cd frontend")
    print("   npm run dev")
    print("\n3. Open http://localhost:3000 in your browser")
    print("\n📖 For more information, see the README.md file")

if __name__ == "__main__":
    main()




