from typing import Any, Callable

from .models import AgentSpec, Subtask
from .orchestrator import RunnerAdapter


class FunctionRunnerAdapter(RunnerAdapter):
    """Small universal adapter. Supply a callable(agent, task, context)->result.

    This keeps AgentOrchestrator independent from AgentRunner internals while
    making integration straightforward.
    """

    def __init__(self, fn: Callable[[AgentSpec, Subtask, dict[str, Any]], Any]):
        self.fn = fn

    def run(self, agent: AgentSpec, task: Subtask, context: dict[str, Any]) -> Any:
        return self.fn(agent, task, context)
