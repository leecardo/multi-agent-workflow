"""K12 工作流路由函数。"""

from __future__ import annotations

from src.state import WorkflowState


def route_by_intent(state: WorkflowState) -> str:
    """根据意图选择业务节点；需要澄清时直接进入输出节点。"""
    if state.get("requires_clarification"):
        return "finalize_output"

    intent = state.get("intent")
    if intent == "teaching_design":
        return "teaching_design"
    if intent == "homework":
        return "homework"
    if intent == "student_tutor":
        return "student_tutor"
    if intent == "learning_analytics":
        return "learning_analytics"
    return "finalize_output"
