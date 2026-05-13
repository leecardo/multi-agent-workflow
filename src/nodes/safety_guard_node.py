"""安全合规 Agent 节点。"""

from __future__ import annotations

from typing import Any

from src.agents.agent_registry import SAFETY_GUARD_AGENT
from src.agents.safety_guard_agent import SafetyGuardAgent
from src.state import WorkflowState


def safety_guard_node(state: WorkflowState) -> dict[str, Any]:
    """检查业务输出是否符合 K12 教育安全边界。"""
    result = SafetyGuardAgent().run(state)
    safety_status = result.metadata.get("status", "pass")
    safety_notes = result.metadata.get("reason")

    update: dict[str, Any] = {
        "current_agent": SAFETY_GUARD_AGENT,
        "safety_status": safety_status,
        "safety_notes": safety_notes,
        "results": {"safety_guard": result.metadata},
        "metadata": {"safety_checked": True},
    }

    if safety_status == "block":
        update["final_output"] = result.output
    elif safety_status == "needs_rewrite":
        update["agent_output"] = result.output

    return update
