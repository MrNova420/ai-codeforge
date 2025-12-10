#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / 'config.yaml'
TEMPLATE_PATH = Path(__file__).parent / 'config_template.yaml'

def setup_config():
    if not CONFIG_PATH.exists():
        print("No config.yaml found. Setting up for first-time use...")
        shutil.copy(TEMPLATE_PATH, CONFIG_PATH)
        print("A config.yaml file has been created. Please enter your API keys and preferences.")
        with open(CONFIG_PATH, 'r') as f:
            lines = f.readlines()
        with open(CONFIG_PATH, 'w') as f:
            for line in lines:
                if 'YOUR_OPENAI_API_KEY_HERE' in line:
                    key = input('Enter your OpenAI API key (or leave blank): ').strip()
                    line = f'openai_api_key: "{key}"\n' if key else line
                if 'YOUR_GEMINI_API_KEY_HERE' in line:
                    key = input('Enter your Gemini API key (or leave blank): ').strip()
                    line = f'gemini_api_key: "{key}"\n' if key else line
                f.write(line)
        print("Config setup complete! You can edit config.yaml anytime to change settings.")
    else:
        print("config.yaml already exists. Edit it to update keys or preferences.")

if __name__ == "__main__":
    setup_config()
