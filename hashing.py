from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Tuple

CHUNK_SIZE = 8192

def compute_hash(file_path: str | Path) -> str:
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    
    hasher = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            hasher.update(chunk)
    
    return hasher.hexdigest()