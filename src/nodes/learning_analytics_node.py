"""学情分析 Agent 节点。"""

from __future__ import annotations

from typing import Any

from src.agents.agent_registry import LEARNING_ANALYTICS_AGENT
from src.agents.learning_analytics_agent import LearningAnalyticsAgent
from src.state import WorkflowState


def learning_analytics_node(state: WorkflowState) -> dict[str, Any]:
    """生成通用学情分析摘要。"""
    result = LearningAnalyticsAgent().run(state)
    return {
        "current_agent": LEARNING_ANALYTICS_AGENT,
        "selected_agent": LEARNING_ANALYTICS_AGENT,
        "agent_output": result.output,
        "results": {"learning_analytics": {"output": result.output, **result.metadata}},
        "metadata": {"business_agent_completed": LEARNING_ANALYTICS_AGENT},
        "resource_context": result.metadata.get("resource_context", {}),
    }
