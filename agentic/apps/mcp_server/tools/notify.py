from packages.common.bus import Bus
from packages.schema.tool_models import PythonRunIn
from packages.common.logger import get_logger

bus = Bus("redis://localhost:6379/0")


def send(message: dict) -> dict:
    bus.publish("notify", message)
    get_logger().info("notify", extra={"message": message})
    return {"ok": True}
