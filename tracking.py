from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

from hashing import compute_hash

baseline_file = "baseline.json"

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def normalize_path(file_path: str | Path) -> str:
    return str(Path(file_path).expanduser().resolve())

def load_baseline(baseline_path: str | Path = baseline_file) -> Dict[str, Any]:
    path = Path(baseline_path)
    if not path.exists():
        return {}
    
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    if not isinstance(data, dict):
        raise ValueError("Baseline file is either corrupt or not a JSON object.")
    
    return data

def save_baseline(data: Dict[str, Any], baseline_path: str | Path = baseline_file) -> None:
    path = Path(baseline_path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)

def add_file(file_path: str | Path, baseline_path: str | Path = baseline_file) -> str:
    normalize = normalize_path(file_path)
    digest = compute_hash(normalize)

    data = load_baseline(baseline_path)
    data[normalize] = {
        "SHA256": digest,
        "added_at": data.get(normalize, {}).get("added_at", utc_now_iso()),
        "updated_at": utc_now_iso(),
        "last_verified_at": data.get(normalize, {}).get("last_verified_at", None),
    }

    save_baseline(data, baseline_path)
    return digest

def remove_file(file_path: str | Path, baseline_path: str | Path = baseline_file) -> bool:
    normalize = normalize_path(file_path)
    data = load_baseline(baseline_path)
    existed = normalize in data
    if existed:
        del data[normalize]
        save_baseline(data, baseline_path)
    return existed

def list_files(baseline_path: str | Path = baseline_file) -> List[str]:
    data = load_baseline(baseline_path)
    return sorted(data.keys())

@dataclass
class ScanResult:
    path: str
    status: str
    expected: str | None = None
    actual: str | None = None
    message: str | None = None

def scan_files(baseline_path: str | Path = baseline_file) -> List[ScanResult]:
    data = load_baseline(baseline_path)
    results: List[ScanResult] = []

    any_verified_at = utc_now_iso()
    anything_changed = False

    for file_path, meta in data.items():
        expected = meta.get("SHA256")
        p =  Path(file_path)

        if not p.exists():
            results.append(ScanResult(path=file_path, status="Missing", expected=expected))
            anything_changed = True
            continue

        try:
            actual = compute_hash(file_path)
        except Exception as e:
            results.append(ScanResult(path=file_path, status="Error", expected=expected, message=str(e)))
            anything_changed = True
            continue

        if actual == expected:
            results.append(ScanResult(path=file_path, status="OK", expected=expected, actual=actual))
        else:
            results.append(ScanResult(path=file_path, status="Changed", expected=expected, actual=actual))
            anything_changed = True

        meta["last_verified_at"] = any_verified_at
    save_baseline(data, baseline_path)
    
    return results