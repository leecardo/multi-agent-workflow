"""K12 教育 Agent 包。"""

from src.agents.agent_registry import (
    HOMEWORK_AGENT,
    INTENT_TO_AGENT,
    LEARNING_ANALYTICS_AGENT,
    SAFETY_GUARD_AGENT,
    STUDENT_TUTOR_AGENT,
    TEACHING_DESIGN_AGENT,
)
from src.agents.base_agent import AgentResult, BaseEducationAgent
from src.agents.homework_agent import HomeworkAgent
from src.agents.learning_analytics_agent import LearningAnalyticsAgent
from src.agents.safety_guard_agent import SafetyGuardAgent
from src.agents.student_tutor_agent import StudentTutorAgent
from src.agents.teaching_design_agent import TeachingDesignAgent

__all__ = [
    "AgentResult",
    "BaseEducationAgent",
    "HOMEWORK_AGENT",
    "HomeworkAgent",
    "INTENT_TO_AGENT",
    "LEARNING_ANALYTICS_AGENT",
    "LearningAnalyticsAgent",
    "SAFETY_GUARD_AGENT",
    "STUDENT_TUTOR_AGENT",
    "SafetyGuardAgent",
    "StudentTutorAgent",
    "TEACHING_DESIGN_AGENT",
    "TeachingDesignAgent",
]
