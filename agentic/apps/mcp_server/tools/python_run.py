import io
import os
import runpy
import sys
import uuid
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any, Dict

from packages.common.hashing import sha256_bytes

BASE = Path("/runs")


def run(payload: Dict[str, Any]) -> Dict[str, Any]:
    run_id = payload.get("run_id", "test")
    step_id = payload.get("step_id", "step")
    call_dir = BASE / run_id / step_id / "pyexec" / str(uuid.uuid4())
    work_dir = call_dir / "work"
    out_dir = call_dir / "out"
    os.makedirs(work_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    entrypoint = payload.get("entrypoint", "main.py")
    code = payload.get("code")
    files = payload.get("files", [])

    for f in files:
        path = work_dir / f["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(f.get("content", b""))

    if entrypoint == "inline":
        entrypoint = "main.py"
        with open(work_dir / entrypoint, "w", encoding="utf-8") as fh:
            fh.write(code or "")

    argv = [entrypoint] + payload.get("args", [])
    stdout, stderr = io.StringIO(), io.StringIO()
    rc = 0
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            sys.argv = argv
            runpy.run_path(str(work_dir / entrypoint), run_name="__main__")
    except SystemExit as e:  # capture exit code
        rc = int(e.code or 0)
    except Exception as e:  # pragma: no cover
        stderr.write(str(e))
        rc = 1

    produced = []
    for path in out_dir.rglob("*"):
        if path.is_file():
            produced.append({"path": str(path.relative_to(call_dir)),
                             "sha256": sha256_bytes(path.read_bytes()),
                             "size": path.stat().st_size})

    return {
        "return_code": rc,
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "produced_files": produced,
    }
