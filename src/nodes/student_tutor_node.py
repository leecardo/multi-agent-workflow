"""学生答疑 Agent 节点。"""

from __future__ import annotations

from typing import Any

from src.agents.agent_registry import STUDENT_TUTOR_AGENT
from src.agents.student_tutor_agent import StudentTutorAgent
from src.state import WorkflowState


def student_tutor_node(state: WorkflowState) -> dict[str, Any]:
    """为学生提供启发式答疑。"""
    result = StudentTutorAgent().run(state)
    return {
        "current_agent": STUDENT_TUTOR_AGENT,
        "selected_agent": STUDENT_TUTOR_AGENT,
        "agent_output": result.output,
        "results": {"student_tutor": {"output": result.output, **result.metadata}},
        "metadata": {"business_agent_completed": STUDENT_TUTOR_AGENT},
        "resource_context": result.metadata.get("resource_context", {}),
    }
