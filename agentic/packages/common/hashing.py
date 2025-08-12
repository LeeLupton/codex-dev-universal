import hashlib
import json
from pathlib import Path
from typing import Optional


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def chain_hash(prev: Optional[str], record: dict) -> str:
    payload = (prev or "") + json.dumps(record, sort_keys=True)
    return sha256_bytes(payload.encode())
