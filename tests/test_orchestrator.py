from agent_orchestrator import AgentOrchestrator, AgentRegistry, AgentSpec, CapabilityRouter, OrchestrationPlan, Subtask
from agent_orchestrator.adapters import FunctionRunnerAdapter


def test_routes_by_capability_and_dependencies():
    registry = AgentRegistry()
    registry.register(AgentSpec("writer", {"write"}, cost_weight=0.2))
    registry.register(AgentSpec("coder", {"code"}, quality_weight=1.2))
    router = CapabilityRouter(registry)

    calls = []
    def run(agent, task, context):
        calls.append((agent.name, task.id))
        return task.id

    plan = OrchestrationPlan(
        "goal",
        [
            Subtask("a", "code", {"code"}),
            Subtask("b", "write", {"write"}, dependencies=["a"]),
        ],
    )
    result = AgentOrchestrator(router, FunctionRunnerAdapter(run)).execute(plan)
    assert result.status == "completed"
    assert calls == [("coder", "a"), ("writer", "b")]


def test_fallback_agent_is_used():
    registry = AgentRegistry()
    registry.register(AgentSpec("a1", {"x"}, quality_weight=2))
    registry.register(AgentSpec("a2", {"x"}, quality_weight=1))
    router = CapabilityRouter(registry)

    def run(agent, task, context):
        if agent.name == "a1":
            raise RuntimeError("fail")
        return "ok"

    plan = OrchestrationPlan("goal", [Subtask("t", "x", {"x"}, max_fallbacks=1)])
    result = AgentOrchestrator(router, FunctionRunnerAdapter(run)).execute(plan)
    assert result.status == "completed"
    assert result.assignments["t"] == "a2"


def test_dependency_deadlock_fails():
    registry = AgentRegistry()
    registry.register(AgentSpec("a", {"x"}))
    router = CapabilityRouter(registry)
    plan = OrchestrationPlan("goal", [Subtask("t", "x", {"x"}, dependencies=["missing"])])
    result = AgentOrchestrator(router, FunctionRunnerAdapter(lambda a, t, c: None)).execute(plan)
    assert result.status == "failed"
