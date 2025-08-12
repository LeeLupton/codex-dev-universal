from typing import List, Optional
from pydantic import BaseModel

class DriveSearchIn(BaseModel):
    query: str
    limit: int = 5

class DriveFile(BaseModel):
    id: str
    name: str

class DriveSearchOut(BaseModel):
    files: List[DriveFile]

class WebSearchIn(BaseModel):
    query: str

class WebResult(BaseModel):
    title: str
    url: str
    snippet: str

class WebSearchOut(BaseModel):
    results: List[WebResult]

class PythonRunIn(BaseModel):
    entrypoint: str
    code: Optional[str] = None
    args: List[str] = []
    timeout_sec: int = 30
    allow_network: bool = False
    allowed_hosts: List[str] = []
    files: List[dict] = []

class PythonRunOut(BaseModel):
    return_code: int
    stdout: str
    stderr: str
    produced_files: List[dict]
    metrics: dict
