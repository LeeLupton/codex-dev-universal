import subprocess
from pathlib import Path

from .base import Runtime


class ProcessRuntime(Runtime):
    def submit(self, kind: str, env: dict, workspace: str) -> None:
        script = Path("workers") / kind / "main.py"
        subprocess.Popen(["python", str(script)], cwd=workspace, env=env)
