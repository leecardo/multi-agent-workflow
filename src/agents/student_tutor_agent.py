"""学生答疑 Agent。"""

from __future__ import annotations

from src.agents.agent_registry import STUDENT_TUTOR_AGENT
from src.agents.base_agent import AgentResult, BaseEducationAgent
from src.config import get_config
from src.services import ResourceService
from src.state import WorkflowState


class StudentTutorAgent(BaseEducationAgent):
    """为学生提供启发式答疑。"""

    name = STUDENT_TUTOR_AGENT
    description = "面向学生的启发式答疑 Agent"

    def run(self, state: WorkflowState) -> AgentResult:
        """生成学生可理解的答疑引导。"""
        config = get_config()
        grade = state.get("grade") or "对应年级"
        subject = state.get("subject") or "这个学科"
        topic = state.get("topic") or state.get("raw_input") or state.get("task")
        student_id = state.get("user_id") or config.default_student_id
        resource_context = ResourceService().get_student_tutor_context(
            grade=grade,
            subject=subject,
            topic=topic,
            student_id=student_id,
        )
        student_profile = resource_context["student_profile"]
        question_bank = resource_context["question_bank"]
        output = f"""我们先不急着直接给答案，一起拆解「{topic}」。

## 第一步：找已知条件
请先圈出题目中的数量、关系或关键词，尤其注意：{question_bank['question_types'][0]}。

## 第二步：确定目标
想一想：题目最终让你求什么？它和已知条件之间有什么联系？

## 第三步：选择方法
在{subject}里，这类问题通常可以从“定义/公式/图示/方程/分步推理”中选择一种方法。

## 第四步：避开常见错误
你最近容易卡在：{"、".join(student_profile['recent_wrong_topics'][:2]) or question_bank['common_mistakes'][0]}。

## 同类练习建议
先做 1 道{question_bank['question_types'][1]}，再做 1 道只改变条件顺序的变式题。
"""
        return AgentResult(
            output=output,
            metadata={"topic": topic, "resource_context": resource_context},
        )
