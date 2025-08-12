import uvicorn
from fastapi import FastAPI
from . import api, ws, db
from .settings import settings
from packages.common.bus import Bus

app = FastAPI()
app.include_router(api.router)
app.include_router(ws.router)

@app.on_event("startup")
def on_startup() -> None:
    db.init_db()
    Bus(settings.REDIS_URL)  # initialize connection


if __name__ == "__main__":
    uvicorn.run("apps.gateway.main:app", host="0.0.0.0", port=settings.API_PORT, reload=False)
