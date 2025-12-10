#!/usr/bin/env python3
"""
Auto-configuration script - Makes system completely self-contained
Detects what's available and configures everything automatically
"""

import os
import subprocess
import yaml
import sys
from pathlib import Path

def check_ollama_installed():
    """Check if Ollama is installed."""
    try:
        result = subprocess.run(['which', 'ollama'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_ollama_running():
    """Check if Ollama is running."""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        return response.status_code == 200
    except:
        return False

def get_ollama_models():
    """Get list of pulled models."""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        return []
    except:
        return []

def start_ollama():
    """Try to start Ollama in background."""
    try:
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL,
                        start_new_session=True)
        import time
        time.sleep(2)  # Give it time to start
        return check_ollama_running()
    except:
        return False

def pull_model(model_name):
    """Pull a model if not already pulled."""
    try:
        result = subprocess.run(['ollama', 'pull', model_name], 
                              capture_output=True, text=True, timeout=300)
        return result.returncode == 0
    except:
        return False

def configure_all_agents(config_path, model_name):
    """Configure all 23 agents - universally works with ANY model."""
    
    # All agents get the same model - simple and universal
    # User can manually edit config.yaml later if they want different models per agent
    all_agents = [
        "helix", "aurora", "felix", "sage", "ember", "orion",
        "atlas", "mira", "vex", "sol", "echo",
        "nova", "quinn", "blaze", "ivy", "zephyr",
        "pixel", "script", "turbo", "sentinel", "link",
        "patch", "pulse"
    ]
    
    config_assignments = {agent: model_name for agent in all_agents}
    
    # Read existing config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Configure all agents
    if 'agent_models' not in config:
        config['agent_models'] = {}
    
    config['agent_models'] = config_assignments
    
    # Set Ollama URL
    config['ollama_url'] = 'http://localhost:11434'
    
    # Save config
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    return True

def install_ollama_auto():
    """Auto-install Ollama without user interaction."""
    print("   📥 Installing Ollama automatically...")
    try:
        # Install via snap (works on Ubuntu/most Linux)
        result = subprocess.run(
            ['sudo', '-n', 'snap', 'install', 'ollama'],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            return True
        
        # If snap doesn't work, try downloading and installing directly
        print("   📥 Trying alternative installation method...")
        subprocess.run(
            ['curl', '-fsSL', 'https://ollama.ai/install.sh'],
            capture_output=True,
            stdout=subprocess.PIPE
        )
        result = subprocess.run(
            ['sh'],
            input=subprocess.run(['curl', '-fsSL', 'https://ollama.ai/install.sh'], 
                               capture_output=True).stdout,
            capture_output=True,
            timeout=120
        )
        return result.returncode == 0
    except:
        return False

def main():
    """Smart setup - detects what you have, asks what you want, does it automatically."""
    print("\n🤖 SMART SETUP")
    print("=" * 60)
    
    config_path = Path(__file__).parent / 'config.yaml'
    
    # STEP 1: Check what's installed
    print("\n📋 Detecting what you have...")
    
    ollama_installed = check_ollama_installed()
    ollama_running = check_ollama_running() if ollama_installed else False
    existing_models = get_ollama_models() if ollama_running else []
    
    print(f"   Ollama: {'✅ Installed' if ollama_installed else '❌ Not installed'}")
    if ollama_installed:
        print(f"   Service: {'✅ Running' if ollama_running else '❌ Not running'}")
    if existing_models:
        print(f"   Models: ✅ {len(existing_models)} found ({', '.join(existing_models[:3])})")
    
    # STEP 2: Install Ollama if needed (AUTOMATIC IN THIS SESSION)
    if not ollama_installed:
        print("\n❓ Ollama not found. Want me to install it? (FREE, runs AI locally)")
        response = input("   Install Ollama? [Y/n]: ").strip().lower()
        if response in ['', 'y', 'yes']:
            print("   📥 Installing Ollama (requires sudo password)...")
            result = subprocess.run(['sudo', 'snap', 'install', 'ollama'], check=False)
            if result.returncode == 0:
                print("   ✅ Installed!")
                ollama_installed = True
            else:
                print("   ❌ Failed to install")
                return False
        else:
            print("   Skipped. Run 'sudo snap install ollama' when ready.")
            return False
    
    # STEP 3: Start Ollama if needed (AUTOMATIC)
    if not ollama_running:
        print("\n📋 Starting Ollama service...")
        started = start_ollama()
        if started:
            print("   ✅ Started!")
            ollama_running = True
            import time
            time.sleep(2)
            existing_models = get_ollama_models()
        else:
            print("   ⚠️  Couldn't auto-start. Trying manual...")
            subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            import time
            time.sleep(3)
            if check_ollama_running():
                print("   ✅ Started!")
                ollama_running = True
                existing_models = get_ollama_models()
            else:
                print("   ❌ Please run 'ollama serve' in another terminal, then press Enter")
                input()
                if not check_ollama_running():
                    return False
                existing_models = get_ollama_models()
    
    # STEP 4: Choose model (or use existing)
    print("\n📋 Choosing model...")
    
    if existing_models:
        print(f"\n   You have {len(existing_models)} model(s):")
        for i, model in enumerate(existing_models, 1):
            print(f"   {i}. {model}")
        print(f"   {len(existing_models)+1}. Download a new model")
        
        choice = input(f"\n   Which to use? [1-{len(existing_models)+1}]: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(existing_models):
            selected_model = existing_models[int(choice)-1]
            print(f"   ✅ Using: {selected_model}")
        else:
            # Download new
            selected_model = None
    else:
        selected_model = None
    
    # Download if needed
    if not selected_model:
        # Let user type ANY model name they want
        print("\n   📥 Enter a model name to download")
        print("   Popular choices: mistral, codellama, llama2, deepseek-coder, phi")
        print("   (Add size like: mistral:7b, codellama:13b, llama2:70b)")
        print("\n   💡 See all models: https://ollama.ai/library")
        
        model_name = input("\n   Model name: ").strip()
        
        if not model_name:
            model_name = "mistral:7b"  # Default only if they press Enter with nothing
            print(f"   Using default: {model_name}")
        
        selected_model = model_name
        
        print(f"\n   📥 Downloading {selected_model}...")
        print("   (This happens automatically, just wait)")
        result = subprocess.run(['ollama', 'pull', selected_model], check=False)
        
        if result.returncode == 0:
            print(f"   ✅ Downloaded!")
        else:
            print(f"   ❌ Download failed - model might not exist")
            print(f"   Check available models: https://ollama.ai/library")
            return False
    
    # STEP 5: Configure agents (AUTOMATIC)
    print(f"\n📋 Configuring 23 agents with {selected_model}...")
    
    if configure_all_agents(config_path, selected_model):
        print("   ✅ All set!")
    else:
        print("   ❌ Config failed")
        return False
    
    # DONE!
    print("\n" + "=" * 60)
    print("✅  READY!")
    print(f"\n   • 23 AI agents configured")
    print(f"   • Using: {selected_model}")
    print(f"   • 100% FREE & PRIVATE")
    print("\n🚀 Run: ./run")
    print("=" * 60 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
