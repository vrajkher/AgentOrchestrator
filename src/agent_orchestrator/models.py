from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentSpec:
    name: str
    capabilities: set[str]
    cost_weight: float = 1.0
    quality_weight: float = 1.0
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Subtask:
    id: str
    goal: str
    required_capabilities: set[str] = field(default_factory=set)
    dependencies: list[str] = field(default_factory=list)
    preferred_agent: str | None = None
    max_fallbacks: int = 1
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class OrchestrationPlan:
    goal: str
    subtasks: list[Subtask]


@dataclass
class OrchestrationResult:
    goal: str
    status: str
    subtask_results: dict[str, Any] = field(default_factory=dict)
    assignments: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
