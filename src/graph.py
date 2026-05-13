"""
K12 教育多智能体工作流图定义。

核心流程：用户请求 -> 意图识别 -> 业务 Agent -> 安全合规 -> 输出结果。
"""

from __future__ import annotations

from typing import Any, Optional

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from src.nodes import (
    finalize_output_node,
    homework_node,
    intent_classifier_node,
    learning_analytics_node,
    route_by_intent,
    safety_guard_node,
    student_tutor_node,
    teaching_design_node,
)
from src.state import WorkflowState


BUSINESS_NODES = (
    "teaching_design",
    "homework",
    "student_tutor",
    "learning_analytics",
)


def create_workflow_graph(checkpointer: Optional[SqliteSaver] = None) -> StateGraph:
    """
    创建 K12 教育多智能体工作流图。

    Args:
        checkpointer: 状态持久化检查点（可选）

    Returns:
        编译后的工作流图
    """
    builder = StateGraph(WorkflowState)

    builder.add_node("intent_classifier", intent_classifier_node)
    builder.add_node("teaching_design", teaching_design_node)
    builder.add_node("homework", homework_node)
    builder.add_node("student_tutor", student_tutor_node)
    builder.add_node("learning_analytics", learning_analytics_node)
    builder.add_node("safety_guard", safety_guard_node)
    builder.add_node("finalize_output", finalize_output_node)

    builder.add_edge(START, "intent_classifier")
    builder.add_conditional_edges(
        "intent_classifier",
        route_by_intent,
        {
            "teaching_design": "teaching_design",
            "homework": "homework",
            "student_tutor": "student_tutor",
            "learning_analytics": "learning_analytics",
            "finalize_output": "finalize_output",
        },
    )

    for node_name in BUSINESS_NODES:
        builder.add_edge(node_name, "safety_guard")

    builder.add_edge("safety_guard", "finalize_output")
    builder.add_edge("finalize_output", END)

    if checkpointer:
        return builder.compile(checkpointer=checkpointer)
    return builder.compile()


def get_default_graph() -> StateGraph:
    """获取默认 K12 教育工作流图。"""
    return create_workflow_graph()


def run_workflow(
    task: str,
    initial_state: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    执行 K12 教育工作流。

    Args:
        task: 用户请求
        initial_state: 初始状态（可选），可传入 user_role、grade、subject 等字段

    Returns:
        最终状态
    """
    graph = get_default_graph()
    state: dict[str, Any] = dict(initial_state or {})
    state.update(
        {
            "task": task,
            "raw_input": state.get("raw_input") or task,
            "current_agent": None,
            "messages": state.get("messages") or [HumanMessage(content=task)],
            "user_role": state.get("user_role", "unknown"),
            "user_id": state.get("user_id"),
            "grade": state.get("grade"),
            "subject": state.get("subject"),
            "topic": state.get("topic"),
            "intent": None,
            "intent_confidence": None,
            "missing_fields": [],
            "requires_clarification": False,
            "clarification_question": None,
            "selected_agent": None,
            "agent_output": None,
            "safety_status": None,
            "safety_notes": None,
            "final_output": None,
            "results": state.get("results", {}),
            "metadata": state.get("metadata", {}),
            "resource_context": state.get("resource_context", {}),
            "task_state": state.get("task_state"),
        }
    )

    return graph.invoke(state)


if __name__ == "__main__":
    test_task = "帮我设计七年级数学一元一次方程教案"

    print("开始执行 K12 教育工作流...")
    print(f"任务: {test_task}")
    print("-" * 50)

    result = run_workflow(test_task, {"user_role": "teacher"})

    print("工作流执行完成")
    print("最终状态:")
    print(f"  当前智能体: {result.get('current_agent')}")
    print(f"  意图: {result.get('intent')}")
    print(f"  业务 Agent: {result.get('selected_agent')}")
    print(f"  安全状态: {result.get('safety_status')}")
    print(f"  最终输出: {result.get('final_output')}")
