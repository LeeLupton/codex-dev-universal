from pathlib import Path


def safe_join(base: Path, *paths: str) -> Path:
    p = (base.joinpath(*paths)).resolve()
    if not str(p).startswith(str(base.resolve())):
        raise ValueError("path escapes base")
    return p


def allow_network(host: str, allowed: list[str]) -> bool:
    return host in allowed
