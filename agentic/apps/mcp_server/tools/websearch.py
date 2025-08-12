# Stub web search tool

def search(payload: dict) -> dict:
    query = payload.get("query", "")
    return {"results": [f"Result for {query}"]}
