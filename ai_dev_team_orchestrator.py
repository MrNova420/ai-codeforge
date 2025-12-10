#!/usr/bin/env python3
import subprocess
import os
import sys
import threading
from pathlib import Path

AGENT_FILES = [
    'planner_designer_agents.md',
    'critic_judge_agents.md',
    'developer_agents.md',
    'developer_assistant_agents.md',
    'debugger_fixer_agent.md',
    'tester_agent.md',
    'overseer_agent.md',
]
AGENT_DIR = Path(__file__).parent

# Map agent names to CLI commands (default to gemini, can be extended)
AGENT_CLI = {
    'aurora': 'gemini', 'felix': 'gemini', 'sage': 'gemini', 'ember': 'gemini', 'orion': 'gemini',
    'atlas': 'gemini', 'mira': 'gemini', 'vex': 'gemini', 'sol': 'gemini', 'echo': 'gemini',
    'nova': 'gemini', 'quinn': 'gemini', 'blaze': 'gemini', 'ivy': 'gemini', 'zephyr': 'gemini',
    'pixel': 'gemini', 'script': 'gemini', 'turbo': 'gemini', 'sentinel': 'gemini', 'link': 'gemini',
    'patch': 'gemini', 'pulse': 'gemini', 'helix': 'gemini',
}

AGENT_LIST = list(AGENT_CLI.keys())


def read_agent_profiles():
    profiles = {}
    for fname in AGENT_FILES:
        fpath = AGENT_DIR / fname
        if fpath.exists():
            with open(fpath) as f:
                profiles[fname] = f.read()
    return profiles


def launch_agent(agent_name, cli_cmd='gemini'):
    """Launch an agent subprocess and return the Popen object."""
    proc = subprocess.Popen([cli_cmd, agent_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc


def agent_interaction(agent_name, proc):
    print(f"\n--- {agent_name.upper()} SESSION ---")
    def read_output():
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(f"[{agent_name}] {line}", end='')
    t = threading.Thread(target=read_output, daemon=True)
    t.start()
    try:
        while True:
            user_input = input(f"({agent_name})> ")
            if user_input.strip().lower() in {'exit', 'quit'}:
                proc.terminate()
                break
            proc.stdin.write(user_input + '\n')
            proc.stdin.flush()
    except KeyboardInterrupt:
        proc.terminate()
        print(f"\n{agent_name} session ended.")


def main():
    print("Ultimate AI Dev Team Orchestrator\n")
    print("Agents available:")
    for idx, name in enumerate(AGENT_LIST, 1):
        print(f"  {idx}. {name}")
    print("\nModes:")
    print("  1. Team mode (all agents in one session)")
    print("  2. Solo mode (choose individual agent)")
    mode = input("Select mode [1/2]: ").strip()
    if mode == '1':
        # Team mode: launch Helix (Overseer) and let user interact
        print("\n[Team Mode] Launching Helix (Overseer)...")
        proc = launch_agent('helix', AGENT_CLI['helix'])
        agent_interaction('helix', proc)
    elif mode == '2':
        print("\nSelect agent by number:")
        for idx, name in enumerate(AGENT_LIST, 1):
            print(f"  {idx}. {name}")
        sel = input("Agent #: ").strip()
        try:
            agent_name = AGENT_LIST[int(sel)-1]
        except Exception:
            print("Invalid selection.")
            return
        print(f"\nLaunching {agent_name}...")
        proc = launch_agent(agent_name, AGENT_CLI[agent_name])
        agent_interaction(agent_name, proc)
    else:
        print("Invalid mode.")

if __name__ == "__main__":
    main()
