"""学情分析 Agent。"""

from __future__ import annotations

from src.agents.agent_registry import LEARNING_ANALYTICS_AGENT
from src.agents.base_agent import AgentResult, BaseEducationAgent
from src.config import get_config
from src.services import ResourceService
from src.state import WorkflowState


class LearningAnalyticsAgent(BaseEducationAgent):
    """生成通用学情分析。"""

    name = LEARNING_ANALYTICS_AGENT
    description = "面向教师、班主任、教务和家长的学情分析 Agent"

    def run(self, state: WorkflowState) -> AgentResult:
        """生成学情分析摘要。"""
        config = get_config()
        topic = state.get("topic") or state.get("raw_input") or state.get("task")
        subject = state.get("subject") or "相关学科"
        class_id = state.get("metadata", {}).get("class_id") or config.default_class_id
        resource_context = ResourceService().get_learning_analytics_context(
            class_id=class_id,
            subject=subject,
        )
        metrics = resource_context["metrics"]
        exam_summary = resource_context["exam_summary"]
        homework_summary = resource_context["homework_summary"]
        recent_scores = metrics['recent_scores'] or exam_summary['score_trend']
        output = f"""# {subject}学情分析：{topic}

## 总体判断
最近 {len(recent_scores)} 次成绩表现为：{" / ".join(str(score) for score in recent_scores)}。

## 重点关注
1. 薄弱知识点：{"、".join(metrics['top_weak_points'][:2])}。
2. 高频错误类型：{"、".join(homework_summary['wrong_causes'])}。
3. 完成情况：最近作业完成率约 {int(homework_summary['completion_rate'] * 100)}%。

## 教学建议
- 下一节课安排 5-10 分钟集中讲解 {exam_summary['weak_points'][0]}。
- 对薄弱学生提供同类基础题巩固。
- 对掌握较好的学生安排变式和综合任务。

## 家校沟通摘要
建议向家长反馈具体可行动建议，避免笼统评价或负面标签。
"""
        return AgentResult(
            output=output,
            metadata={"topic": topic, "resource_context": resource_context},
        )
