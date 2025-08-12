import hashlib
import json
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def chain_log(record: Any, prev: str = "") -> str:
    blob = prev + json.dumps(record, sort_keys=True)
    return sha256_bytes(blob.encode())
