from packages.common.bus import publish


def send(payload: dict) -> dict:
    publish("notifications", payload)
    return {"sent": True}
