"""意图识别节点：规则优先，预留 LLM 分类扩展点。"""

from __future__ import annotations

import re
from typing import Any

from src.agents.agent_registry import INTENT_TO_AGENT
from src.state import WorkflowState

INTENT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "teaching_design": (
        "教案",
        "备课",
        "课件",
        "教学设计",
        "课堂活动",
        "说课",
        "教学目标",
    ),
    "homework": ("作业", "练习", "题目", "试卷", "变式题", "分层作业", "出题"),
    "student_tutor": ("不会做", "怎么解", "讲一下", "思路", "错题", "知识点", "解析"),
    "learning_analytics": (
        "成绩",
        "错题率",
        "薄弱点",
        "班级分析",
        "学情",
        "进步",
        "退步",
        "报告",
    ),
}

SUBJECTS = (
    "语文",
    "数学",
    "英语",
    "物理",
    "化学",
    "生物",
    "历史",
    "地理",
    "政治",
    "道德与法治",
    "科学",
)
GRADE_PATTERN = re.compile(
    r"(小学[一二三四五六1-6]年级|[一二三四五六七八九高][年级一二三]?[一二三]?年级|[1-9]年级|高[一二三])"
)

REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "teaching_design": ("grade", "subject", "topic"),
    "homework": ("grade", "subject", "topic"),
    "student_tutor": ("subject", "topic"),
    "learning_analytics": ("topic",),
}

FIELD_NAMES: dict[str, str] = {
    "grade": "年级",
    "subject": "学科",
    "topic": "主题/知识点/数据范围",
}


def _text_from_state(state: WorkflowState) -> str:
    return state.get("raw_input") or state.get("task") or ""


def _match_intent(
    text: str, user_role: str
) -> tuple[str | None, float, dict[str, Any]]:
    scores: dict[str, int] = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        scores[intent] = sum(1 for keyword in keywords if keyword in text)

    if user_role == "student" and any(
        keyword in text for keyword in ("不会", "怎么", "讲", "错题")
    ):
        scores["student_tutor"] += 2
    if user_role == "teacher" and any(
        keyword in text for keyword in ("教案", "备课", "出题", "作业")
    ):
        scores["teaching_design"] += 1 if "教案" in text or "备课" in text else 0
        scores["homework"] += 1 if "作业" in text or "出题" in text else 0

    best_intent, best_score = max(scores.items(), key=lambda item: item[1])
    if best_score == 0:
        return (
            None,
            0.0,
            {"rule_scores": scores, "strategy": "rule_then_llm_placeholder"},
        )

    sorted_scores = sorted(scores.values(), reverse=True)
    confidence = 0.9 if best_score >= 2 else 0.72
    if len(sorted_scores) > 1 and sorted_scores[0] == sorted_scores[1]:
        confidence = 0.55
    return (
        best_intent,
        confidence,
        {"rule_scores": scores, "strategy": "rule_then_llm_placeholder"},
    )


def _extract_slots(text: str) -> dict[str, str | None]:
    grade_match = GRADE_PATTERN.search(text)
    subject = next((item for item in SUBJECTS if item in text), None)

    topic = text
    for keyword in (
        "帮我",
        "请",
        "生成",
        "设计",
        "分析",
        "讲一下",
        "怎么解",
        "作业",
        "教案",
        "练习",
    ):
        topic = topic.replace(keyword, "")
    topic = topic.strip(" ，。！？:：") or None

    return {
        "grade": grade_match.group(0) if grade_match else None,
        "subject": subject,
        "topic": topic,
    }


def _missing_fields(
    intent: str | None, state: WorkflowState, slots: dict[str, str | None]
) -> list[str]:
    if intent is None:
        return []

    missing: list[str] = []
    for field in REQUIRED_FIELDS.get(intent, ()):  # noqa: A001
        value = state.get(field) or slots.get(field)
        if not value:
            missing.append(field)
    return missing


def _clarification_question(
    intent: str | None, missing_fields: list[str]
) -> str | None:
    if intent is None:
        return "请补充你的教育场景，例如是要备课、出题、答疑，还是做学情分析？"
    if not missing_fields:
        return None
    fields = "、".join(FIELD_NAMES[field] for field in missing_fields)
    return f"为了更准确处理，请补充{fields}。"


def intent_classifier_node(state: WorkflowState) -> dict[str, Any]:
    """识别用户请求意图，并抽取基础槽位。"""
    text = _text_from_state(state)
    user_role = state.get("user_role", "unknown")
    intent, confidence, metadata = _match_intent(text, user_role)
    slots = _extract_slots(text)
    missing_fields = _missing_fields(intent, state, slots)
    requires_clarification = intent is None or confidence < 0.6 or bool(missing_fields)
    clarification_question = _clarification_question(intent, missing_fields)

    selected_agent = INTENT_TO_AGENT.get(intent or "")
    result = {
        "intent": intent,
        "confidence": confidence,
        "extracted_slots": slots,
        "needs_clarification": requires_clarification,
        "clarification_question": clarification_question,
        **metadata,
    }

    return {
        "current_agent": "IntentRouterAgent",
        "intent": intent,
        "intent_confidence": confidence,
        "grade": state.get("grade") or slots.get("grade"),
        "subject": state.get("subject") or slots.get("subject"),
        "topic": state.get("topic") or slots.get("topic"),
        "missing_fields": missing_fields,
        "requires_clarification": requires_clarification,
        "clarification_question": clarification_question,
        "selected_agent": selected_agent,
        "results": {"intent_classifier": result},
        "metadata": {"intent_classified": True},
    }
