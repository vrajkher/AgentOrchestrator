# AgentOrchestrator

Universal routing and orchestration layer for AI agents.

## Purpose
AgentOrchestrator takes a goal, decomposes it into subtasks, selects the best registered agent for each subtask, respects dependencies, executes ready tasks through a runner adapter, supports bounded fallback, and merges the results.

## Core flow
`Goal -> Task Decomposer -> Capability Router -> Dependency Scheduler -> Runner Adapter -> Result Merger`

## Features
- Agent-neutral capability registry
- Deterministic score-based routing
- Dependency-aware execution
- Parallel-ready planning model
- Fallback agents
- Cost/quality hints
- Runner adapter contract for AgentRunner integration
- Structured orchestration result

## Quick start
```bash
pip install -e .
python examples/basic_orchestration.py
pytest
```

## Scope
This repo decides WHO should do WHAT and WHEN. Actual tool execution belongs in AgentRunner. Memory/skill retrieval belongs in AgentLibrarian. Governance and approval belong in the later security layer.
