from packages.common.hashing import chain_log

# Event append stub

def append(run_id: str, event: str, payload: dict) -> str:
    record = {"run_id": run_id, "event": event, "payload": payload}
    return chain_log(record)
