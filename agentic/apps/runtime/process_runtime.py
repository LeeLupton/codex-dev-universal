import subprocess
import sys
from pathlib import Path


class ProcessRuntime:
    def submit(self, kind: str, env: dict, workspace: str) -> None:
        worker = Path(__file__).resolve().parents[2] / "workers" / kind / "main.py"
        subprocess.Popen([sys.executable, str(worker)], cwd=workspace, env={**env})
