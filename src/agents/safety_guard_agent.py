"""内容安全与合规 Agent。"""

from __future__ import annotations

from src.agents.agent_registry import SAFETY_GUARD_AGENT
from src.agents.base_agent import AgentResult, BaseEducationAgent
from src.state import WorkflowState

BLOCK_KEYWORDS = ("自杀", "自残", "色情", "暴力伤害", "泄露身份证", "泄题", "考试答案")
REWRITE_KEYWORDS = ("笨", "差生", "没救", "蠢", "懒死")


class SafetyGuardAgent(BaseEducationAgent):
    """检查 K12 输出是否符合安全合规边界。"""

    name = SAFETY_GUARD_AGENT
    description = "内容安全与合规 Agent"

    def run(self, state: WorkflowState) -> AgentResult:
        """返回安全检查结论。"""
        content = state.get("agent_output") or ""
        raw_input = state.get("raw_input") or state.get("task") or ""
        combined = f"{raw_input}\n{content}"

        if any(keyword in combined for keyword in BLOCK_KEYWORDS):
            notes = "请求或输出可能涉及未成年人安全、隐私、违法或考试违规内容。"
            return AgentResult(
                output="抱歉，这个请求涉及安全或合规风险，不能直接处理。建议联系教师、监护人或学校相关负责人获得帮助。",
                metadata={"status": "block", "reason": notes},
            )

        if any(keyword in combined for keyword in REWRITE_KEYWORDS):
            notes = (
                "内容包含不适合教育场景的负面标签，建议改为具体、温和、可行动的表达。"
            )
            rewritten = content
            for keyword in REWRITE_KEYWORDS:
                rewritten = rewritten.replace(keyword, "需要更多支持")
            return AgentResult(
                output=rewritten,
                metadata={"status": "needs_rewrite", "reason": notes},
            )

        return AgentResult(
            output=content,
            metadata={"status": "pass", "reason": "内容通过基础安全合规检查。"},
        )
