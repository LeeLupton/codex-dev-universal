from pathlib import Path


def init(repo: str) -> dict:
    path = Path(repo)
    path.mkdir(parents=True, exist_ok=True)
    return {"ok": True}


def add_all(repo: str) -> dict:
    return {"ok": True}


def commit(repo: str, message: str) -> dict:
    return {"ok": True, "message": message}
