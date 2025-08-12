import uvicorn
from fastapi import FastAPI

from .api import router as api_router
from .db import init_db
from .ws import router as ws_router

app = FastAPI()
app.include_router(api_router)
app.include_router(ws_router)

@app.on_event("startup")
async def startup_event():
    init_db()

if __name__ == "__main__":
    uvicorn.run("apps.gateway.main:app", host="0.0.0.0", port=8080, reload=False)
