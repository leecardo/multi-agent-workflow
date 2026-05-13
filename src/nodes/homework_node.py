"""作业与练习生成 Agent 节点。"""

from __future__ import annotations

from typing import Any

from src.agents.agent_registry import HOMEWORK_AGENT
from src.agents.homework_agent import HomeworkAgent
from src.state import WorkflowState


def homework_node(state: WorkflowState) -> dict[str, Any]:
    """生成 K12 作业与练习。"""
    result = HomeworkAgent().run(state)
    return {
        "current_agent": HOMEWORK_AGENT,
        "selected_agent": HOMEWORK_AGENT,
        "agent_output": result.output,
        "results": {"homework": {"output": result.output, **result.metadata}},
        "metadata": {"business_agent_completed": HOMEWORK_AGENT},
        "resource_context": result.metadata.get("resource_context", {}),
    }
