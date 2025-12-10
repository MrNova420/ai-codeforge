#!/usr/bin/env python3
"""
PROPER First-Time Setup - User-Friendly & Automated
Handles EVERYTHING from scratch - no assumptions
"""

import os
import sys
import subprocess
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(num, total, text):
    print(f"[{num}/{total}] {text}")

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        print(f"   You have: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True

def setup_venv():
    """Create virtual environment"""
    venv_path = PROJECT_ROOT / "venv"
    if venv_path.exists():
        print("✅ Virtual environment exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], 
                      check=True, capture_output=True)
        print("✅ Virtual environment created")
        return True
    except:
        print("❌ Failed to create virtual environment")
        return False

def install_packages():
    """Install required packages"""
    venv_path = PROJECT_ROOT / "venv"
    pip_exe = venv_path / "bin" / "pip"
    
    print("📦 Installing packages...")
    packages = ["rich", "pyyaml", "requests", "openai", "google-generativeai"]
    
    try:
        subprocess.run(
            [str(pip_exe), "install", "-q"] + packages,
            check=True,
            capture_output=True
        )
        print("✅ Packages installed")
        return True
    except:
        print("❌ Failed to install packages")
        return False

def check_ollama():
    """Check if Ollama is available"""
    try:
        result = subprocess.run(['which', 'ollama'], capture_output=True)
        return result.returncode == 0
    except:
        return False

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        return response.status_code == 200
    except:
        return False

def get_ollama_models():
    """Get list of available Ollama models"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            return [m['name'] for m in response.json().get('models', [])]
        return []
    except:
        return []

def start_ollama():
    """Try to start Ollama service"""
    print("\n🚀 Starting Ollama service...")
    try:
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL,
                        start_new_session=True)
        time.sleep(3)
        if check_ollama_running():
            print("✅ Ollama started")
            return True
        else:
            print("⚠️  Ollama may not be running")
            return False
    except:
        print("❌ Could not start Ollama")
        return False

def download_model(model_name):
    """Download an Ollama model"""
    print(f"\n📥 Downloading {model_name}...")
    print("    This may take several minutes...")
    try:
        result = subprocess.run(
            ['ollama', 'pull', model_name],
            capture_output=False,
            timeout=600
        )
        if result.returncode == 0:
            print(f"✅ {model_name} downloaded")
            return True
        else:
            print(f"❌ Failed to download {model_name}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Download timed out")
        return False
    except:
        print("❌ Download failed")
        return False

def setup_local_mode():
    """Setup for local Ollama models"""
    print_header("LOCAL MODE SETUP")
    
    # Check if Ollama is installed
    if not check_ollama():
        print("❌ Ollama not found\n")
        print("Install Ollama:")
        print("  • Visit: https://ollama.ai")
        print("  • Or run: curl https://ollama.ai/install.sh | sh\n")
        input("Press Enter after installing Ollama...")
        
        if not check_ollama():
            print("❌ Still can't find Ollama")
            return None
    
    print("✅ Ollama installed")
    
    # Check if Ollama is running
    if not check_ollama_running():
        print("\n⚠️  Ollama service not running")
        choice = input("Start it now? [Y/n]: ").strip().lower()
        if choice != 'n':
            if not start_ollama():
                print("\n❌ Could not start Ollama")
                print("   Try manually: ollama serve")
                return None
    else:
        print("✅ Ollama running")
    
    # Check existing models
    existing = get_ollama_models()
    
    print("\n📋 Available models on your system:")
    if existing:
        for i, model in enumerate(existing, 1):
            print(f"   {i}. {model}")
    else:
        print("   (none)")
    
    # Choose model
    print("\n🎯 Choose a model:")
    print("   1. Use existing model")
    print("   2. Download recommended (mistral:7b - 4GB)")
    print("   3. Download coding model (codellama:7b - 4GB)")
    print("   4. Enter custom model name")
    
    choice = input("\nChoice [1-4]: ").strip()
    
    if choice == '1':
        if not existing:
            print("❌ No models available")
            return None
        print("\nSelect model:")
        for i, model in enumerate(existing, 1):
            print(f"   {i}. {model}")
        idx = input(f"Choice [1-{len(existing)}]: ").strip()
        try:
            model = existing[int(idx) - 1]
            return {'type': 'local', 'model': model}
        except:
            print("❌ Invalid choice")
            return None
    
    elif choice == '2':
        if download_model('mistral:7b'):
            return {'type': 'local', 'model': 'mistral:7b'}
        return None
    
    elif choice == '3':
        if download_model('codellama:7b'):
            return {'type': 'local', 'model': 'codellama:7b'}
        return None
    
    elif choice == '4':
        model = input("Enter model name (e.g., llama2:7b): ").strip()
        if model:
            if download_model(model):
                return {'type': 'local', 'model': model}
        return None
    
    return None

def setup_api_mode():
    """Setup for API-based models (OpenAI/Gemini)"""
    print_header("API MODE SETUP")
    
    print("Choose provider:")
    print("   1. OpenAI (GPT-4, GPT-3.5)")
    print("   2. Google Gemini")
    print("   3. Both")
    
    choice = input("\nChoice [1-3]: ").strip()
    
    config = {'type': 'api'}
    
    if choice in ['1', '3']:
        print("\n🔑 OpenAI API Key:")
        print("   Get from: https://platform.openai.com/api-keys")
        api_key = input("   Enter key: ").strip()
        config['openai_key'] = api_key
        config['openai_model'] = 'gpt-4'
    
    if choice in ['2', '3']:
        print("\n🔑 Google Gemini API Key:")
        print("   Get from: https://makersuite.google.com/app/apikey")
        api_key = input("   Enter key: ").strip()
        config['gemini_key'] = api_key
        config['gemini_model'] = 'gemini-pro'
    
    return config if ('openai_key' in config or 'gemini_key' in config) else None

def create_config(setup_config):
    """Create config.yaml with user choices"""
    import yaml
    
    # All 23 agents
    all_agents = [
        "helix", "aurora", "felix", "sage", "ember", "orion",
        "atlas", "mira", "vex", "sol", "echo", "nova", "quinn",
        "blaze", "ivy", "zephyr", "pixel", "script", "turbo",
        "sentinel", "link", "patch", "pulse"
    ]
    
    if setup_config['type'] == 'local':
        model = setup_config['model']
        config = {
            'openai_api_key': '',
            'gemini_api_key': '',
            'ollama_url': 'http://localhost:11434',
            'ollama_model': model,
            'agent_models': {agent: model for agent in all_agents}
        }
    else:
        # API mode
        openai_model = setup_config.get('openai_model', '')
        gemini_model = setup_config.get('gemini_model', '')
        default_model = openai_model or gemini_model
        
        config = {
            'openai_api_key': setup_config.get('openai_key', ''),
            'gemini_api_key': setup_config.get('gemini_key', ''),
            'ollama_url': 'http://localhost:11434',
            'ollama_model': '',
            'agent_models': {agent: default_model for agent in all_agents}
        }
    
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print("\n✅ Configuration saved")
    return True

def main():
    """Main setup flow"""
    clear_screen()
    print("\n" + "="*60)
    print("  🚀 AI DEV TEAM - FIRST-TIME SETUP")
    print("="*60)
    print("\n  Welcome! This wizard will set up everything you need.")
    print("  It's designed to be EASY - just follow the prompts.\n")
    
    # Step 1: Check Python
    print_step(1, 6, "Checking Python")
    if not check_python():
        sys.exit(1)
    
    # Step 2: Setup venv
    print_step(2, 6, "Setting up virtual environment")
    if not setup_venv():
        sys.exit(1)
    
    # Step 3: Install packages
    print_step(3, 6, "Installing packages")
    if not install_packages():
        sys.exit(1)
    
    # Step 4: Choose mode
    print_step(4, 6, "Choose AI backend")
    print("\nHow do you want to run AI models?\n")
    print("   1. 🆓 LOCAL (Free, private, needs ~4GB RAM)")
    print("      • Uses Ollama")
    print("      • Runs on your computer")
    print("      • Completely free")
    print()
    print("   2. ☁️  API (Paid, fast, no local resources)")
    print("      • Uses OpenAI or Google Gemini")
    print("      • Requires API key")
    print("      • Costs money per use")
    
    mode = input("\nChoice [1-2]: ").strip()
    
    # Step 5: Setup chosen mode
    print_step(5, 6, "Configuring AI backend")
    
    if mode == '1':
        setup_config = setup_local_mode()
    elif mode == '2':
        setup_config = setup_api_mode()
    else:
        print("❌ Invalid choice")
        sys.exit(1)
    
    if not setup_config:
        print("\n❌ Setup failed")
        sys.exit(1)
    
    # Step 6: Create config
    print_step(6, 6, "Saving configuration")
    create_config(setup_config)
    
    # Done!
    print("\n" + "="*60)
    print("  ✅ SETUP COMPLETE!")
    print("="*60)
    print("\n  Your AI Dev Team is ready to use!")
    print("\n  Next steps:")
    print("    1. Run: ./run")
    print("    2. Choose Team or Solo mode")
    print("    3. Start building!\n")
    print("  All 23 agents are configured and ready.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
