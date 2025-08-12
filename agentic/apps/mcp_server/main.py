import uvicorn
from .server import app
from packages.common.logger import get_logger
import os

bind = os.getenv("MCP_BIND", "0.0.0.0:7000")

if __name__ == "__main__":
    host, port = bind.split(":")
    uvicorn.run(app, host=host, port=int(port))
