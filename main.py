from __future__ import annotations

import argparse
import sys
from pathlib import Path

from hashing import compute_hash, verify_hash

def cmd_hash(args: argparse.Namespace) -> int:
    file_path = args.file
    try:
        digest = compute_hash(file_path)
    except FileNotFoundError as e:
        print(f"No file {e}", file=sys.stderr)
        return 1
    
    print(f"File: {file_path}")
    print(f"SHA-256: {digest}")
    return 0

