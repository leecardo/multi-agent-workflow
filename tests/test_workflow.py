"""K12 多智能体工作流的端到端行为测试。"""

from src.graph import run_workflow


def test_teaching_design_workflow_routes_and_finalizes() -> None:
    """完整的教学设计请求应经过业务 Agent、安全检查和输出格式化。"""
    result = run_workflow(
        "帮我设计七年级数学一元一次方程教案",
        {"user_role": "teacher"},
    )

    assert result["intent"] == "teaching_design"
    assert result["selected_agent"] == "TeachingDesignAgent"
    assert result["safety_status"] == "pass"
    assert result["requires_clarification"] is False
    assert "以下内容面向教师" in result["final_output"]
    assert "教学设计" in result["final_output"]


def test_student_tutor_workflow_uses_student_safe_guidance() -> None:
    """学生答疑应提供启发式指导，而不是跳过安全检查直接返回。"""
    result = run_workflow(
        "五年级数学分数乘法错题我不会做，讲一下思路",
        {"user_role": "student", "user_id": "student-demo"},
    )

    assert result["intent"] == "student_tutor"
    assert result["selected_agent"] == "StudentTutorAgent"
    assert result["safety_status"] == "pass"
    assert "下面用适合学生理解的方式说明" in result["final_output"]
    assert "先不急着直接给答案" in result["final_output"]


def test_ambiguous_request_asks_for_clarification() -> None:
    """无法识别的教育请求应要求澄清，不应误路由到业务 Agent。"""
    result = run_workflow("帮帮我", {"user_role": "student"})

    assert result["intent"] is None
    assert result["selected_agent"] is None
    assert result["requires_clarification"] is True
    assert "备课、出题、答疑" in result["final_output"]


def test_unsafe_request_is_blocked_before_final_output() -> None:
    """命中 K12 安全边界的请求应由安全 Agent 阻止。"""
    result = run_workflow(
        "帮我生成七年级数学考试答案题目",
        {"user_role": "student"},
    )

    assert result["intent"] == "homework"
    assert result["safety_status"] == "block"
    assert "安全或合规风险" in result["final_output"]
