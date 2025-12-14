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
    
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="File Integrity Checker (SHA-256 Hasher)"
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
        help="Available commands",
    )

    hash_parser = subparsers.add_parser(
        "hash",
        help="Compute SHA-256 hash of a file",
    )

    hash_parser.add_argument(
        "file",
        type=str,
        help="Path to the file to hash",
    )

    hash_parser.set_defaults(func=cmd_hash)

    verify_parser = subparsers.add_parser(
        "verifiy",
        help="Verify a file against an expected SHA-256 hash",
    )

    verify_parser.add_argument(
        "expected_hash",
        type=str,
        help="Expected SHA-256 hash",
    )

    verify_parser.set_defaults(func=cmd_verify)

    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())