from fastapi import FastAPI
from fastapi import FastAPI
from .tools import drive, websearch, python_run, repo_git, notify
from packages.schema.tool_models import DriveSearchIn, WebSearchIn, PythonRunIn

app = FastAPI()


@app.post("/mcp/drive.search")
def drive_search(inp: DriveSearchIn):
    return drive.search(inp)


@app.post("/mcp/web.search")
def web_search(inp: WebSearchIn):
    return websearch.search(inp)


@app.post("/mcp/python.run")
def python_run_api(inp: PythonRunIn):
    return python_run.run(inp)


@app.post("/mcp/repo.git.init")
def repo_init(payload: dict):
    return repo_git.init(payload["repo"])


@app.post("/mcp/repo.git.add_all")
def repo_add(payload: dict):
    return repo_git.add_all(payload["repo"])


@app.post("/mcp/repo.git.commit")
def repo_commit(payload: dict):
    return repo_git.commit(payload["repo"], payload.get("message", ""))


@app.post("/mcp/notify.send")
def notify_send(payload: dict):
    return notify.send(payload)
