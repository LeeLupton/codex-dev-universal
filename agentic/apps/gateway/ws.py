from fastapi import APIRouter, WebSocket
from packages.common.bus import Bus
from .settings import settings

router = APIRouter()
bus = Bus(settings.REDIS_URL)


@router.websocket("/ws/runs/{run_id}")
async def ws_runs(ws: WebSocket, run_id: str):
    await ws.accept()
    def handler(msg):
        ws.send_text(msg)
    bus.subscribe(f"results.{run_id}", lambda m: ws.send_json(m))
