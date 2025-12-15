from __future__ import annotations

import argparse
import sys
from pathlib import Path

from hashing import compute_hash, verify_hash
from tracking import add_file, remove_file, list_files, scan_files

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
    
def cmd_track_add(args: argparse.Namespace) -> int:
    try:
        digest = add_file(args.file)
    except FileNotFoundError as e:
        print("No file {e}", file=sys.stderr)
        return 1
    
    print(f"Tracking: {args.file}")
    print(f"SHA-256:   {digest}")
    return 0

def cmd_track_list(args: argparse.Namespace) -> int:
    files = list_files()
    if not files:
        print("No tracked files yet. Use: python main.py track add <file>")
        return 0
    
    print("Tracked files:")
    for f in files:
        print(f"- {f}")
    return 0

def cmd_track_remove(args: argparse.Namespace) -> int:
    removed = remove_file(args.file)
    if removed:
        print(f"Removed from tracking: {args.file}")
        return 0
    else:
        print(f"Not tracked: {args.file}")
        return 0
    
def cmd_track_scan(args: argparse.Namespace) -> int:
    results = scan_files()

    if not results:
        print(f"No tracked files yet. Use: python main.py track add <file>")
        return 0
    
    any_bad = False
    for r in results:
        if r.status == "OK":
            print(f"OK  {r.path}")
        elif r.status == "Changed":
            any_bad = True
            print(f"Changed {r.path}")
        elif r.status == "Missing":
            any_bad = True
            print(f"Missing {r.path}")
        else:
            any_bad = True
            print(f"Error {r.path} ({r.message})")
    
    return 2 if any_bad else 0

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
        "verify",
        help="Verify a file against an expected SHA-256 hash",
    )

    verify_parser.add_argument(
        "file",
        type=str,
        help="Path to the file to verify"
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