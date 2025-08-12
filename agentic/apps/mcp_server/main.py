import uvicorn

from apps.gateway.settings import settings

if __name__ == "__main__":
    host, port = settings.MCP_HOST, settings.MCP_PORT
    uvicorn.run("apps.mcp_server.server:app", host=host, port=port)
