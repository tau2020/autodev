from dataclasses import dataclass
from typing import Any, Dict, Optional, List


@dataclass
class Task:
    task_id: int
    description: str
    code: Optional[str] = None
    tests: Optional[str] = None


@dataclass
class Project:
    name: str
    description: str
    tasks: List[Task] = None


@dataclass
class Message:
    sender: str
    recipient: str
    content: str


@dataclass
class AgentContext:
    context_variables: Dict[str, Any]


@dataclass
class Result:
    value: str
    agent: Optional[str] = None
    context_variables: Dict[str, Any] = None


@dataclass
class Response:
    messages: List[Dict[str, Any]]
    agent: Optional[str] = None
    context_variables: Dict[str, Any] = None
