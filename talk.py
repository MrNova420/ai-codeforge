#!/usr/bin/env python3
"""
AI CodeForge - Natural Language Interface
Just talk to it! No code required.

Usage:
    ./talk                           # Start chat
    ./talk "create a login system"   # Single command
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from natural_interface import main

if __name__ == "__main__":
    main()
