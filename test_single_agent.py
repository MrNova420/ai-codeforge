#!/usr/bin/env python3
"""
Test single agent interaction - Direct and fast
"""

import sys
import yaml
import requests
from pathlib import Path
from orchestrator import AgentProfile, Config

PROJECT_ROOT = Path(__file__).parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

def test_direct_agent():
    """Test agent without orchestrator overhead."""
    print("🤖 Testing Direct Agent Communication\n")
    
    # Load config
    if not CONFIG_PATH.exists():
        print("❌ Config not found. Run: ./setup_proper.py")
        return 1
    
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)
    
    # Create simple agent
    agent = AgentProfile(
        name="Nova",
        role="Senior Backend Developer",
        personality="Pragmatic and efficient",
        strengths="Backend systems, APIs, databases",
        approach="Write clean, tested code",
        model="codellama:7b"
    )
    
    print(f"Agent: {agent.name} ({agent.role})")
    print(f"Model: {config['agent_models']['nova']}\n")
    
    # Test question
    question = "Write a Python function to check if a number is prime. Keep it simple, just the function."
    
    print(f"Question: {question}\n")
    print("Thinking...\n")
    
    # Build prompt
    system_prompt = agent.get_system_prompt()
    full_prompt = f"{system_prompt}\n\nUser: {question}\n\nAssistant:"
    
    # Send to Ollama
    try:
        response = requests.post(
            f"{config['ollama_url']}/api/generate",
            json={
                "model": config['agent_models']['nova'],
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "num_predict": 300,
                    "temperature": 0.7
                }
            },
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get('response', '').strip()
            
            print("Response:")
            print("-" * 60)
            print(answer)
            print("-" * 60)
            
            # Stats
            eval_duration = result.get('eval_duration', 0) / 1e9  # Convert to seconds
            tokens = result.get('eval_count', 0)
            
            print(f"\n✅ Success!")
            print(f"   Tokens: {tokens}")
            print(f"   Time: {eval_duration:.2f}s")
            if tokens > 0:
                print(f"   Speed: {tokens/eval_duration:.1f} tokens/sec")
            
            return 0
        else:
            print(f"❌ HTTP {response.status_code}")
            return 1
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out (120s)")
        print("   Model may be too slow or prompt too complex")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(test_direct_agent())
