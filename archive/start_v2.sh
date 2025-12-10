#!/bin/bash
# Launch Ultimate AI Dev Team V2

cd "$(dirname "$0")"

echo "🚀 Launching Ultimate AI Dev Team V2..."
echo ""

# Activate venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 orchestrator_v2.py
