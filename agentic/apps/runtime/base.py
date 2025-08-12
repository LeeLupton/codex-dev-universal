from typing import Dict, Protocol


class Runtime(Protocol):
    def submit(self, kind: str, env: Dict, workspace: str) -> None: ...
