from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .models import AgentSpec, OrchestrationPlan, OrchestrationResult, Subtask
from .router import CapabilityRouter


class RunnerAdapter(ABC):
    @abstractmethod
    def run(self, agent: AgentSpec, task: Subtask, context: dict[str, Any]) -> Any:
        raise NotImplementedError


class AgentOrchestrator:
    def __init__(self, router: CapabilityRouter, runner: RunnerAdapter):
        self.router = router
        self.runner = runner

    def _ready(self, task: Subtask, completed: set[str]) -> bool:
        return all(dep in completed for dep in task.dependencies)

    def execute(self, plan: OrchestrationPlan) -> OrchestrationResult:
        result = OrchestrationResult(goal=plan.goal, status="running")
        pending = {task.id: task for task in plan.subtasks}
        completed: set[str] = set()

        while pending:
            ready = [task for task in pending.values() if self._ready(task, completed)]
            if not ready:
                result.status = "failed"
                result.errors.append("Dependency deadlock or missing dependency")
                return result

            progress = False
            for task in ready:
                excluded: set[str] = set()
                last_error: Exception | None = None
                attempts = 0
                while attempts <= task.max_fallbacks:
                    attempts += 1
                    try:
                        agent = self.router.choose(task, exclude=excluded)
                    except Exception as exc:
                        last_error = exc
                        break

                    result.assignments[task.id] = agent.name
                    context = {
                        "goal": plan.goal,
                        "dependency_results": {
                            dep: result.subtask_results.get(dep) for dep in task.dependencies
                        },
                    }
                    try:
                        output = self.runner.run(agent, task, context)
                        result.subtask_results[task.id] = output
                        completed.add(task.id)
                        pending.pop(task.id, None)
                        progress = True
                        last_error = None
                        break
                    except Exception as exc:
                        last_error = exc
                        excluded.add(agent.name)

                if last_error is not None:
                    result.status = "failed"
                    result.errors.append(f"{task.id}: {last_error}")
                    return result

            if not progress and pending:
                result.status = "failed"
                result.errors.append("No execution progress")
                return result

        result.status = "completed"
        return result
