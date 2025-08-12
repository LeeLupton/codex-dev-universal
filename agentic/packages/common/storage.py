from pathlib import Path
from typing import Union

BASE = Path("/runs")


def write_artifact(run_id: str, path: str, data: Union[str, bytes]) -> Path:
    dest = BASE / run_id / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(dest, mode) as fh:
        fh.write(data)
    return dest
