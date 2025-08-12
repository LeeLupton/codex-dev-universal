from apps.runtime.process_runtime import ProcessRuntime
from apps.runtime.docker_runtime import DockerRuntime
from .settings import settings


def get_runtime():
    if settings.RUNTIME == "docker":
        return DockerRuntime()
    return ProcessRuntime()
