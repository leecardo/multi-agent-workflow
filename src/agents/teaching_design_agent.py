"""教学设计 Agent。"""

from __future__ import annotations

from src.agents.base_agent import AgentResult, BaseEducationAgent
from src.agents.agent_registry import TEACHING_DESIGN_AGENT
from src.services import ResourceService
from src.state import WorkflowState


class TeachingDesignAgent(BaseEducationAgent):
    """生成 K12 教学设计。"""

    name = TEACHING_DESIGN_AGENT
    description = "面向教师的教学设计 Agent"

    def run(self, state: WorkflowState) -> AgentResult:
        """生成结构化教学设计。"""
        grade = state.get("grade") or "未指定年级"
        subject = state.get("subject") or "未指定学科"
        topic = state.get("topic") or state.get("raw_input") or state.get("task")
        resource_context = ResourceService().get_teaching_design_context(
            grade=grade,
            subject=subject,
            topic=topic,
        )
        curriculum = resource_context["curriculum"]
        textbook_sections = resource_context["textbook_sections"]
        lesson_plan_template = resource_context["lesson_plan_template"]
        recommended_resources = resource_context["recommended_resources"]

        output = f"""# {grade}{subject}教学设计：{topic}

## 教学目标
1. {curriculum['goals'][0]}
2. {curriculum['goals'][1]}
3. {curriculum['goals'][2] if len(curriculum['goals']) > 2 else '通过课堂互动提升表达、合作与反思能力。'}

## 教学重难点
- 重点：{textbook_sections[0]['title']}、{curriculum['keywords'][0]}。
- 难点：{textbook_sections[-1]['title']}与知识迁移应用。

## 教学流程
1. 导入：结合教材章节「{textbook_sections[0]['title']}」引出{topic}。
2. 探究：围绕{lesson_plan_template['teaching_methods'][0]}组织学生观察、讨论、归纳。
3. 讲解：结合「{textbook_sections[-1]['title']}」示范典型例题与关键步骤。
4. 练习：依据课程标准关键词 {"、".join(curriculum['keywords'][:3])} 设计分层训练。
5. 总结：请学生复述本节课关键知识与易错点。

## 资源参考
- 推荐案例：{recommended_resources[0]['title']}
- 活动资源：{recommended_resources[1]['title']}

## 作业建议
- 基础巩固：完成 3-5 道围绕「{curriculum['keywords'][0]}」的基础题。
- 提升拓展：完成 1-2 道综合应用题，并口头说明解题依据。
"""
        return AgentResult(
            output=output,
            metadata={"topic": topic, "resource_context": resource_context},
        )
