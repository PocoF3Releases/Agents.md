#!/usr/bin/env python3
"""Run local knowledge checks without network access or hosted CI."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
commands = [
    [sys.executable, "scripts/validate_knowledge.py", "--json"],
    [sys.executable, "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"],
    ["git", "diff", "--check"],
    ["git", "diff", "--cached", "--check"],
]
for command in commands:
    result = subprocess.run(command, cwd=root)
    if result.returncode:
        sys.exit(result.returncode)
