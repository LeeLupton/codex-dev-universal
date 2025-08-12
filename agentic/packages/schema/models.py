from typing import Dict, List, Literal, Optional
from pydantic import BaseModel

Kind = Literal["plan","research","codegen","eval","repo","notify","tool"]

class Step(BaseModel):
    id: str
    kind: Kind
    input: Dict
    depends_on: List[str] = []
    tool: Optional[str] = None

class Plan(BaseModel):
    run_id: str
    goal: str
    steps: List[Step]

class WorkItem(BaseModel):
    run_id: str
    step_id: str
    kind: Kind
    input: Dict
    reply_to: str
    tool: Optional[str] = None

class WorkResult(BaseModel):
    run_id: str
    step_id: str
    ok: bool
    output: Dict = {}
    logs: Optional[str] = None
