import httpx
from .settings import settings

base = f"http://{settings.MCP_HOST}:{settings.MCP_PORT}/mcp"


def call(tool: str, payload: dict) -> dict:
    resp = httpx.post(f"{base}/{tool}", json=payload, timeout=30.0)
    resp.raise_for_status()
    return resp.json()
