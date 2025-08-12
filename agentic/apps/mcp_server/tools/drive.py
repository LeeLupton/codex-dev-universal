# Stub Google Drive tool

def search(payload: dict) -> dict:
    query = payload.get("query", "")
    return {"files": [{"id": "1", "name": f"Result for {query}"}]}

def get(payload: dict) -> dict:
    return {"file": {"id": payload.get("id"), "name": "dummy"}}

def download(payload: dict) -> dict:
    return {"content": ""}

def upload(payload: dict) -> dict:
    return {"id": "uploaded"}
