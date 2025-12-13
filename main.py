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

def cmd_verify(args: argparse.Namespace) -> int:
    file_path = args.file
    expected_hash = args.expected_hash

    try:
        is_match, actual_hash = verify_hash(file_path, expected_hash)
    except FileNotFoundError as e:
        print(f"No file {e}", file=sys.stderr)
        return 1
    
    print(f"File:     {file_path}")
    print(f"Expected: {expected_hash}")
    print(f"Actual:   {actual_hash}")
    print()

    if is_match: 
        print("Integrity check PASSED (hashes match)")
        return 0
    else:
        print("Integrity check FAILED (hahed do NOT match)")
        return 2
    
    