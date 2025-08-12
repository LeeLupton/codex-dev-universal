from pathlib import Path
from .hashing import sha256_file


def manifest_dir(base: Path) -> list[dict]:
    items = []
    for p in base.rglob("*"):
        if p.is_file():
            items.append({"path": str(p.relative_to(base)), "sha256": sha256_file(p), "size": p.stat().st_size})
    return items
