"""
K12 教育多智能体工作流示例。

演示通用流程：用户请求 -> 意图识别 -> 业务 Agent -> 安全合规 -> 输出结果。
"""

import sys
from pathlib import Path


def setup_path() -> None:
    """设置项目根目录到 Python 路径。"""
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


def print_result(title: str, result: dict) -> None:
    """打印工作流执行结果。"""
    print(title)
    print(f"  意图: {result.get('intent')}")
    print(f"  业务 Agent: {result.get('selected_agent')}")
    print(f"  是否需要澄清: {result.get('requires_clarification')}")
    print(f"  安全状态: {result.get('safety_status')}")
    print("  最终输出:")
    print(result.get("final_output"))
    print()


def main() -> None:
    """主函数：演示 K12 教育工作流执行。"""
    setup_path()

    # 延迟导入，避免 E402 错误
    from src.graph import create_workflow_graph, run_workflow
    from src.state import TaskState

    print("=== K12 教育多智能体工作流示例 ===")
    print()

    examples = [
        (
            "示例1：教师备课",
            "帮我设计七年级数学一元一次方程教案",
            {"user_role": "teacher"},
        ),
        (
            "示例2：作业生成",
            "生成10道五年级数学分数乘法练习题",
            {"user_role": "teacher", "user_id": "student-demo"},
        ),
        (
            "示例3：学生答疑",
            "这道数学错题我不会做，讲一下思路",
            {"user_role": "student", "user_id": "student-demo", "grade": "五年级", "subject": "数学"},
        ),
        (
            "示例4：学情分析",
            "帮我分析最近三次数学测试的学情",
            {"user_role": "teacher", "subject": "数学", "metadata": {"class_id": "class-demo"}},
        ),
    ]

    for title, task, initial_state in examples:
        print(f"任务: {task}")
        result = run_workflow(task, initial_state)
        print(f"  资源上下文键: {list((result.get('resource_context') or {}).keys())}")
        print_result(title, result)

    print("示例5：创建工作流图")
    graph = create_workflow_graph()
    print(f"工作流图类型: {type(graph)}")
    print(f"可用节点: {list(graph.nodes.keys()) if hasattr(graph, 'nodes') else 'N/A'}")
    print()

    print("示例6：使用任务状态模型")
    task_state = TaskState(
        task_id="k12-task-001",
        status="running",
        progress=30,
        assigned_agents=[
            "IntentRouterAgent",
            "TeachingDesignAgent",
            "SafetyGuardAgent",
        ],
    )
    print(f"任务ID: {task_state.task_id}")
    print(f"状态: {task_state.status}")
    print(f"进度: {task_state.progress}%")
    print(f"分配的智能体: {task_state.assigned_agents}")
    print()

    print("示例完成！")


if __name__ == "__main__":
    main()
