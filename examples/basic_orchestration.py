from agent_orchestrator import AgentOrchestrator, AgentRegistry, AgentSpec, CapabilityRouter, OrchestrationPlan, Subtask
from agent_orchestrator.adapters import FunctionRunnerAdapter

registry = AgentRegistry()
registry.register(AgentSpec("cheap-agent", {"summarize"}, cost_weight=0.2, quality_weight=0.8))
registry.register(AgentSpec("coding-agent", {"code", "summarize"}, cost_weight=1.0, quality_weight=1.2))
router = CapabilityRouter(registry)


def run(agent, task, context):
    return {"agent": agent.name, "task": task.id, "goal": task.goal, "context": context}

plan = OrchestrationPlan(
    goal="Build and summarize",
    subtasks=[
        Subtask("code", "Write code", {"code"}),
        Subtask("summary", "Summarize result", {"summarize"}, dependencies=["code"]),
    ],
)

result = AgentOrchestrator(router, FunctionRunnerAdapter(run)).execute(plan)
print(result)
