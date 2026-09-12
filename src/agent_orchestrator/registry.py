from .models import AgentSpec


class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, AgentSpec] = {}

    def register(self, agent: AgentSpec) -> None:
        self._agents[agent.name] = agent

    def get(self, name: str) -> AgentSpec:
        return self._agents[name]

    def enabled(self) -> list[AgentSpec]:
        return [a for a in self._agents.values() if a.enabled]
