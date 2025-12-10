#!/usr/bin/env python3
"""
Quick Test Script - Verify AI Dev Team is working
Tests basic functionality without full orchestrator
"""

import sys
import yaml
import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

def test_config():
    """Test configuration exists."""
    print("1. Testing configuration...")
    if not CONFIG_PATH.exists():
        print("   ❌ Config not found. Run: ./setup_proper.py")
        return False
    
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)
    
    if not config.get('agent_models'):
        print("   ❌ No agent models configured")
        return False
    
    print(f"   ✅ Config found with {len(config['agent_models'])} agents")
    return True


def test_ollama():
    """Test Ollama connection."""
    print("\n2. Testing Ollama...")
    
    try:
        # Check if Ollama is running
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code != 200:
            print("   ❌ Ollama not responding")
            return False
        
        models = response.json().get('models', [])
        print(f"   ✅ Ollama running with {len(models)} models")
        
        # List models
        for model in models:
            print(f"      - {model['name']}")
        
        return True
    
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to Ollama")
        print("      Install: curl https://ollama.ai/install.sh | sh")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_simple_generation():
    """Test simple text generation."""
    print("\n3. Testing model generation...")
    
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'codellama:7b',
                'prompt': 'Say hello in 3 words',
                'stream': False,
                'options': {'num_predict': 10}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('response', '').strip()
            print(f"   ✅ Model response: '{generated_text}'")
            return True
        else:
            print(f"   ❌ Status {response.status_code}")
            return False
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_agents():
    """Test agent files exist."""
    print("\n4. Testing agent files...")
    
    agent_files = [
        'overseer_agent.md',
        'planner_designer_agents.md',
        'developer_agents.md',
        'critic_judge_agents.md',
        'tester_agent.md',
        'developer_assistant_agents.md',
        'debugger_fixer_agent.md'
    ]
    
    found = 0
    for agent_file in agent_files:
        if (PROJECT_ROOT / agent_file).exists():
            found += 1
    
    print(f"   ✅ Found {found}/{len(agent_files)} agent definition files")
    return found >= 5  # At least 5 files should exist


def main():
    """Run all tests."""
    print("🧪 AI Dev Team - Quick Test\n" + "="*50)
    
    tests = [
        test_config,
        test_ollama,
        test_simple_generation,
        test_agents
    ]
    
    passed = sum(test() for test in tests)
    total = len(tests)
    
    print("\n" + "="*50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! System is ready.")
        print("   Run: ./run")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("   Run: ./setup_proper.py")
        return 1


if __name__ == '__main__':
    sys.exit(main())
