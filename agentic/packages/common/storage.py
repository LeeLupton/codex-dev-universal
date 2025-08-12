from pathlib import Path
from typing import BinaryIO


def write_artifact(base: Path, run_id: str, path: str, data: bytes) -> Path:
    dest = base / run_id / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest


def read_artifact(base: Path, run_id: str, path: str) -> bytes:
    return (base / run_id / path).read_bytes()
