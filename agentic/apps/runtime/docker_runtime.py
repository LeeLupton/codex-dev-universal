import subprocess

from .base import Runtime


class DockerRuntime(Runtime):
    def submit(self, kind: str, env: dict, workspace: str) -> None:
        image = f"agentic/worker-{kind}:latest"
        subprocess.Popen([
            "docker", "run", "--rm", "--network", "host",
            "-v", f"{workspace}:/workspace", image
        ], env=env)
