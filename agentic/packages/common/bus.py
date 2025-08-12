import json
import redis
from typing import Callable


class Bus:
    def __init__(self, url: str) -> None:
        self.client = redis.Redis.from_url(url, decode_responses=True)

    def publish(self, channel: str, message: dict) -> None:
        self.client.publish(channel, json.dumps(message))

    def subscribe(self, channel: str, handler: Callable[[dict], None]) -> None:
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        for msg in pubsub.listen():
            if msg["type"] == "message":
                handler(json.loads(msg["data"]))
