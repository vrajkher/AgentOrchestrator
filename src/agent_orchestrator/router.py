from .models import AgentSpec, Subtask
from .registry import AgentRegistry


class CapabilityRouter:
    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    def ranked(self, task: Subtask) -> list[AgentSpec]:
        agents = self.registry.enabled()
        if task.preferred_agent:
            agents.sort(key=lambda a: a.name != task.preferred_agent)

        def score(agent: AgentSpec) -> float:
            matched = len(task.required_capabilities & agent.capabilities)
            missing = len(task.required_capabilities - agent.capabilities)
            capability_score = matched * 10 - missing * 100
            return capability_score + agent.quality_weight * 2 - agent.cost_weight

        return sorted(agents, key=score, reverse=True)

    def choose(self, task: Subtask, exclude: set[str] | None = None) -> AgentSpec:
        exclude = exclude or set()
        for agent in self.ranked(task):
            if agent.name in exclude:
                continue
            if task.required_capabilities.issubset(agent.capabilities):
                return agent
        raise RuntimeError(f"No capable agent available for {task.id}")
