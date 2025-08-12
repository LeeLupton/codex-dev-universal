import subprocess


class DockerRuntime:
    def submit(self, kind: str, env: dict, workspace: str) -> None:
        image = f"agentic/worker-{kind}:latest"
        subprocess.Popen([
            "docker", "run", "--rm", "--network", "host", "-v", f"{workspace}:/workspace", image
        ])
