"""最终输出格式化节点。"""

from __future__ import annotations

from typing import Any

from src.state import WorkflowState

ROLE_PREFIX: dict[str, str] = {
    "teacher": "以下内容面向教师，可直接按需调整使用：",
    "student": "下面用适合学生理解的方式说明：",
    "parent": "以下内容面向家长，尽量保持清晰、温和、可操作：",
    "admin": "以下内容面向教务/管理场景：",
}


def finalize_output_node(state: WorkflowState) -> dict[str, Any]:
    """生成最终用户可见输出。"""
    if state.get("final_output"):
        output = state["final_output"]
    elif state.get("requires_clarification"):
        output = state.get("clarification_question") or "请补充更多信息后我再继续处理。"
    elif state.get("safety_status") == "block":
        output = "抱歉，这个请求涉及安全或合规风险，不能直接处理。"
    else:
        prefix = ROLE_PREFIX.get(state.get("user_role", "unknown"), "以下是处理结果：")
        agent_output = (
            state.get("agent_output") or "暂未生成有效结果，请补充更明确的教育场景。"
        )
        output = f"{prefix}\n\n{agent_output}"

    return {
        "current_agent": "finalize_output",
        "final_output": output,
        "results": {"finalize_output": {"output": output}},
        "metadata": {"output_finalized": True},
    }
