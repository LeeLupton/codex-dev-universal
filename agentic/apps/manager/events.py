from packages.common.bus import Bus
from .settings import settings

bus = Bus(settings.REDIS_URL)


def append(run_id: str, event: dict) -> None:
    bus.publish(f"events.{run_id}", event)
