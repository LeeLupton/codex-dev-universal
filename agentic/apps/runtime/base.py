from typing import Protocol, Dict


class Runtime(Protocol):
    def submit(self, kind: str, env: Dict, workspace: str) -> None: ...
