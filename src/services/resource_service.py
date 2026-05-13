"""统一资源服务。"""

from __future__ import annotations

from typing import Any, Callable

from src.config import get_config
from src.repositories import RedisRepository
from src.services.curriculum_service import CurriculumService
from src.services.lesson_plan_service import LessonPlanService
from src.services.learning_analytics_service import LearningAnalyticsService
from src.services.question_bank_service import QuestionBankService
from src.services.student_profile_service import StudentProfileService
from src.services.textbook_service import TextbookService


class ResourceService:
    """负责聚合结构化资源、外部技能和缓存。"""

    def __init__(
        self,
        curriculum_service: CurriculumService | None = None,
        textbook_service: TextbookService | None = None,
        lesson_plan_service: LessonPlanService | None = None,
        question_bank_service: QuestionBankService | None = None,
        student_profile_service: StudentProfileService | None = None,
        learning_analytics_service: LearningAnalyticsService | None = None,
        cache_repository: RedisRepository | None = None,
    ) -> None:
        self.config = get_config()
        self.curriculum_service = curriculum_service or CurriculumService()
        self.textbook_service = textbook_service or TextbookService()
        self.lesson_plan_service = lesson_plan_service or LessonPlanService()
        self.question_bank_service = question_bank_service or QuestionBankService()
        self.student_profile_service = student_profile_service or StudentProfileService()
        self.learning_analytics_service = learning_analytics_service or LearningAnalyticsService()
        self.cache_repository = cache_repository or RedisRepository()

    def _get_or_set(self, key: str, loader: Callable[[], Any]) -> Any:
        if self.config.enable_cache:
            cached = self.cache_repository.get(key)
            if cached is not None:
                return cached
        value = loader()
        if self.config.enable_cache:
            self.cache_repository.set(key, value)
        return value

    def get_teaching_design_context(
        self, *, grade: str, subject: str, topic: str
    ) -> dict[str, Any]:
        """聚合教学设计所需资源。"""
        cache_key = f"teaching:{grade}:{subject}:{topic}"
        return self._get_or_set(
            cache_key,
            lambda: {
                "curriculum": self.curriculum_service.get_standard(grade, subject),
                "textbook_sections": self.textbook_service.get_sections(grade, subject),
                "lesson_plan_template": self.lesson_plan_service.get_template("教学设计"),
                "recommended_resources": self.lesson_plan_service.get_recommended_cases(
                    grade=grade,
                    subject=subject,
                    topic=topic,
                ),
            },
        )

    def get_homework_context(
        self, *, grade: str, subject: str, topic: str, student_id: str | None
    ) -> dict[str, Any]:
        """聚合作业设计所需资源。"""
        cache_key = f"homework:{grade}:{subject}:{topic}:{student_id or 'none'}"
        return self._get_or_set(
            cache_key,
            lambda: {
                "question_bank": self.question_bank_service.get_question_context(grade, subject),
                "homework_summary": self.question_bank_service.get_recent_homework_summary(
                    student_id=student_id
                ),
                "student_profile": (
                    self.student_profile_service.get_profile(student_id)
                    if student_id
                    else None
                ),
            },
        )

    def get_student_tutor_context(
        self, *, grade: str, subject: str, topic: str, student_id: str
    ) -> dict[str, Any]:
        """聚合学生答疑资源。"""
        cache_key = f"student_tutor:{grade}:{subject}:{topic}:{student_id}"
        return self._get_or_set(
            cache_key,
            lambda: {
                "student_profile": self.student_profile_service.get_profile(student_id),
                "question_bank": self.question_bank_service.get_question_context(grade, subject),
                "homework_summary": self.question_bank_service.get_recent_homework_summary(
                    student_id=student_id
                ),
            },
        )

    def get_learning_analytics_context(self, *, class_id: str, subject: str) -> dict[str, Any]:
        """聚合学情分析资源。"""
        cache_key = f"analytics:{class_id}:{subject}"
        return self._get_or_set(
            cache_key,
            lambda: self.learning_analytics_service.get_learning_overview(
                class_id=class_id,
                subject=subject,
            ),
        )
