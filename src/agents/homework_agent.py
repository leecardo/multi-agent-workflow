"""作业与练习生成 Agent。"""

from __future__ import annotations

from src.agents.agent_registry import HOMEWORK_AGENT
from src.agents.base_agent import AgentResult, BaseEducationAgent
from src.config import get_config
from src.services import ResourceService
from src.state import WorkflowState


class HomeworkAgent(BaseEducationAgent):
    """生成 K12 作业与练习。"""

    name = HOMEWORK_AGENT
    description = "面向教师和学生的作业与练习生成 Agent"

    def run(self, state: WorkflowState) -> AgentResult:
        """生成练习题结构。"""
        config = get_config()
        grade = state.get("grade") or "对应年级"
        subject = state.get("subject") or "对应学科"
        topic = state.get("topic") or state.get("raw_input") or state.get("task")
        student_id = state.get("user_id") or config.default_student_id
        resource_context = ResourceService().get_homework_context(
            grade=grade,
            subject=subject,
            topic=topic,
            student_id=student_id,
        )
        question_bank = resource_context["question_bank"]
        homework_summary = resource_context["homework_summary"]
        student_profile = resource_context.get("student_profile")
        output = f"""# {grade}{subject}练习：{topic}

## 题量建议
- 基础题 {question_bank['difficulty_distribution']['basic']} 道
- 提升题 {question_bank['difficulty_distribution']['intermediate']} 道
- 拓展题 {question_bank['difficulty_distribution']['advanced']} 道

## 题型方向
- {question_bank['question_types'][0]}
- {question_bank['question_types'][1]}
- 易错提醒：{question_bank['common_mistakes'][0]}

## 作业反馈参考
- 最近完成率：{int(homework_summary['completion_rate'] * 100)}%
- 近期关注：{"、".join(homework_summary['recent_focus'])}
- 高频错因：{"、".join(homework_summary['wrong_causes'])}

## 个性化建议
- {student_profile['name'] if student_profile else '学生'} 优先巩固：{topic}
- 训练时重点关注：{question_bank['common_mistakes'][0]}
"""
        return AgentResult(
            output=output,
            metadata={"topic": topic, "resource_context": resource_context},
        )
