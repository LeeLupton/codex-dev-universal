from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/ws/runs/{run_id}")
async def ws_runs(ws: WebSocket, run_id: str):
    await ws.accept()
    await ws.send_json({"run_id": run_id, "event": "connected"})
    await ws.close()
