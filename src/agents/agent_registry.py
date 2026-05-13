"""K12 教育 Agent 注册表。"""

from __future__ import annotations


TEACHING_DESIGN_AGENT = "TeachingDesignAgent"
HOMEWORK_AGENT = "HomeworkAgent"
STUDENT_TUTOR_AGENT = "StudentTutorAgent"
LEARNING_ANALYTICS_AGENT = "LearningAnalyticsAgent"
SAFETY_GUARD_AGENT = "SafetyGuardAgent"

INTENT_TO_AGENT: dict[str, str] = {
    "teaching_design": TEACHING_DESIGN_AGENT,
    "homework": HOMEWORK_AGENT,
    "student_tutor": STUDENT_TUTOR_AGENT,
    "learning_analytics": LEARNING_ANALYTICS_AGENT,
}

BUSINESS_INTENTS = set(INTENT_TO_AGENT)
