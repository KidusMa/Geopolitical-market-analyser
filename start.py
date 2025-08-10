#!/usr/bin/env python3
"""
Startup script for Geopolitical Market Analyzer
Runs both the Flask API backend and React frontend
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def run_backend():
    """Run the Flask API backend"""
    print("🚀 Starting Flask API backend...")
    try:
        subprocess.run([sys.executable, "api.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Run the React frontend"""
    print("🌐 Starting React frontend...")
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found. Please run 'npm install' in the frontend directory first.")
        return
    
    try:
        # Check if node_modules exists
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        print("🎨 Starting React development server...")
        subprocess.run(["npm", "start"], cwd=frontend_dir, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
    except FileNotFoundError:
        print("❌ Node.js/npm not found. Please install Node.js first.")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def main():
    """Main startup function"""
    print("🌍 Geopolitical Market Analyzer")
    print("=" * 40)
    
    # Check if required files exist
    if not Path("api.py").exists():
        print("❌ api.py not found. Please ensure you're in the correct directory.")
        return
    
    if not Path("frontend").exists():
        print("❌ frontend directory not found. Please ensure you're in the correct directory.")
        return
    
    print("📋 Starting both backend and frontend...")
    print("💡 Backend will run on http://localhost:5000")
    print("💡 Frontend will run on http://localhost:3000")
    print("💡 Press Ctrl+C to stop both servers")
    print("-" * 40)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(2)
    
    # Start frontend in main thread
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    
    print("👋 Goodbye!")

if __name__ == "__main__":
    main()
