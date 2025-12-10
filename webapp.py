#!/usr/bin/env python3
"""
AI CodeForge Web Application Launcher
Starts both the WebSocket backend and serves the frontend
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import fastapi
        import uvicorn
        return True
    except ImportError:
        print("❌ Missing dependencies!")
        print("\nPlease install required packages:")
        print("  pip install fastapi uvicorn")
        return False

def start_backend():
    """Start the WebSocket backend server."""
    backend_path = Path(__file__).parent / "ui" / "backend" / "websocket_server.py"
    
    if not backend_path.exists():
        print(f"❌ Backend not found: {backend_path}")
        return None
    
    print("🚀 Starting WebSocket backend...")
    process = subprocess.Popen(
        [sys.executable, str(backend_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Give it a moment to start
    time.sleep(2)
    
    if process.poll() is None:
        print("✅ Backend running on http://localhost:8000")
        return process
    else:
        print("❌ Backend failed to start")
        return None

def start_frontend():
    """Start the frontend HTTP server."""
    frontend_path = Path(__file__).parent / "ui" / "frontend"
    
    if not frontend_path.exists():
        print(f"❌ Frontend not found: {frontend_path}")
        return None
    
    print("🌐 Starting frontend server...")
    process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3000"],
        cwd=str(frontend_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Give it a moment to start
    time.sleep(1)
    
    if process.poll() is None:
        print("✅ Frontend running on http://localhost:3000")
        return process
    else:
        print("❌ Frontend failed to start")
        return None

def main():
    """Main launcher function."""
    print("╭─────────────────────────────────────────╮")
    print("│  AI CodeForge Web Application           │")
    print("│  AAA Development Team UI                │")
    print("╰─────────────────────────────────────────╯\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start servers
    backend = start_backend()
    if not backend:
        print("\n❌ Failed to start backend")
        sys.exit(1)
    
    frontend = start_frontend()
    if not frontend:
        print("\n❌ Failed to start frontend")
        backend.terminate()
        sys.exit(1)
    
    print("\n╭─────────────────────────────────────────╮")
    print("│  ✅ AI CodeForge is ready!               │")
    print("├─────────────────────────────────────────┤")
    print("│  🌐 Open: http://localhost:3000         │")
    print("│  📡 API:  http://localhost:8000         │")
    print("│                                         │")
    print("│  Press Ctrl+C to stop                   │")
    print("╰─────────────────────────────────────────╯\n")
    
    # Handle shutdown
    def shutdown(signum, frame):
        print("\n\n🛑 Shutting down...")
        frontend.terminate()
        backend.terminate()
        print("✅ Stopped cleanly")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    
    # Wait for processes
    try:
        while True:
            # Check if processes are still running
            if backend.poll() is not None:
                print("❌ Backend stopped unexpectedly")
                frontend.terminate()
                sys.exit(1)
            
            if frontend.poll() is not None:
                print("❌ Frontend stopped unexpectedly")
                backend.terminate()
                sys.exit(1)
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        shutdown(None, None)

if __name__ == "__main__":
    main()
