from fastapi import FastAPI

from .tools import drive, notify, python_run, repo_git, websearch

app = FastAPI()

@app.post("/mcp/drive.search")
async def drive_search(payload: dict):
    return drive.search(payload)

@app.post("/mcp/web.search")
async def web_search(payload: dict):
    return websearch.search(payload)

@app.post("/mcp/python.run")
async def python_run_action(payload: dict):
    return python_run.run(payload)

@app.post("/mcp/repo.git")
async def repo_git_action(payload: dict):
    return repo_git.run(payload)

@app.post("/mcp/notify.send")
async def notify_send(payload: dict):
    return notify.send(payload)
