"""LLM 客户端占位封装。

当前实现以规则分类为主；当接入 LangChain/OpenAI 等模型时，可在此模块
集中实现 LLM 调用，避免业务节点硬编码模型细节。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LLMClassificationResult:
    """LLM 意图分类结果。"""

    intent: str | None
    confidence: float
    extracted_slots: dict[str, Any]
    needs_clarification: bool
    clarification_question: str | None = None


class LLMClient:
    """LLM 调用封装基类。"""

    def classify_intent(
        self, text: str, context: dict[str, Any]
    ) -> LLMClassificationResult:
        """分类用户意图。

        当前项目尚未配置具体模型，因此该方法返回低置信度结果。
        后续可在这里接入 LangChain/OpenAI，并保持节点层接口不变。
        """
        return LLMClassificationResult(
            intent=None,
            confidence=0.0,
            extracted_slots={},
            needs_clarification=True,
            clarification_question="请补充你的教育场景，例如备课、出题、答疑或学情分析。",
        )
