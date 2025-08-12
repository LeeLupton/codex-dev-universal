from typing import Any, Dict

import httpx

from .settings import settings


async def call(action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"http://{settings.MCP_HOST}:{settings.MCP_PORT}/mcp/{action}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
