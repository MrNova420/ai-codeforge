#!/usr/bin/env python3
"""
SMART Auto-Configuration - No user input, fully automated
Detects what you have and configures everything automatically
"""

import os
import subprocess
import yaml
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

def check_ollama():
    """Check if Ollama exists and is running."""
    try:
        result = subprocess.run(['which', 'ollama'], capture_output=True)
        if result.returncode != 0:
            return False, []
        
        # Check if running
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', [])]
            return True, models
        return False, []
    except:
        return False, []

def get_best_model(available_models):
    """Pick the best available model automatically."""
    # Priority order: coding models > general models
    priority = [
        'deepseek-coder:33b', 'deepseek-coder:6.7b',
        'codellama:34b', 'codellama:13b', 'codellama:7b',
        'phind-codellama:34b', 'wizardcoder:34b',
        'mixtral:8x7b', 'mistral:7b',
        'llama2:70b', 'llama2:13b', 'llama2:7b',
        'llama3.1:8b', 'llama3:8b',
    ]
    
    for model in priority:
        if model in available_models:
            return model
    
    # If nothing from priority, just use first available
    return available_models[0] if available_models else None

def configure_system(model_name):
    """Configure all agents with the model."""
    all_agents = [
        "helix", "aurora", "felix", "sage", "ember", "orion",
        "atlas", "mira", "vex", "sol", "echo", "nova", "quinn",
        "blaze", "ivy", "zephyr", "pixel", "script", "turbo",
        "sentinel", "link", "patch", "pulse"
    ]
    
    config = {
        'openai_api_key': '',
        'gemini_api_key': '',
        'ollama_url': 'http://localhost:11434',
        'ollama_model': model_name,
        'agent_models': {agent: model_name for agent in all_agents}
    }
    
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    return True

def main():
    """Main auto-configuration - fully automated."""
    silent = '--silent' in sys.argv
    fix_only = '--fix-models' in sys.argv
    
    if not silent:
        print("🔧 Auto-configuring...")
    
    # Check Ollama
    running, models = check_ollama()
    
    if not running or not models:
        if not silent:
            print("❌ No Ollama models found")
            print("   Install: https://ollama.ai")
            print("   Then run: ollama pull mistral:7b")
        return False
    
    # Get best available model
    best_model = get_best_model(models)
    
    if not best_model:
        if not silent:
            print("❌ No suitable models found")
        return False
    
    # Configure
    configure_system(best_model)
    
    if not silent:
        print(f"✅ Configured with: {best_model}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
