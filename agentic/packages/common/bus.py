from typing import Dict, Iterable, List

# In-memory bus placeholder
_queue: Dict[str, List[str]] = {}


def publish(channel: str, message: str) -> None:
    _queue.setdefault(channel, []).append(message)


def subscribe(pattern: str) -> Iterable[str]:
    # naive implementation: yield and clear
    msgs = _queue.get(pattern, [])
    _queue[pattern] = []
    for m in msgs:
        yield m
