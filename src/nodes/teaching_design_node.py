"""教学设计 Agent 节点。"""

from __future__ import annotations

from typing import Any

from src.agents.agent_registry import TEACHING_DESIGN_AGENT
from src.agents.teaching_design_agent import TeachingDesignAgent
from src.state import WorkflowState


def teaching_design_node(state: WorkflowState) -> dict[str, Any]:
    """生成结构化教学设计。"""
    result = TeachingDesignAgent().run(state)
    return {
        "current_agent": TEACHING_DESIGN_AGENT,
        "selected_agent": TEACHING_DESIGN_AGENT,
        "agent_output": result.output,
        "results": {"teaching_design": {"output": result.output, **result.metadata}},
        "metadata": {"business_agent_completed": TEACHING_DESIGN_AGENT},
        "resource_context": result.metadata.get("resource_context", {}),
    }
