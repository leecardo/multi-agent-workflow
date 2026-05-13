"""题库服务。"""

from __future__ import annotations

from typing import Any

from src.repositories import PostgresRepository
from src.skills import HomeworkPlatformSkill


class QuestionBankService:
    """聚合题库与作业平台摘要。"""

    def __init__(
        self,
        repository: PostgresRepository | None = None,
        homework_skill: HomeworkPlatformSkill | None = None,
    ) -> None:
        self.repository = repository or PostgresRepository()
        self.homework_skill = homework_skill or HomeworkPlatformSkill()

    def get_question_context(self, grade: str, subject: str) -> dict[str, Any]:
        """获取题库上下文。"""
        return self.repository.get_question_bank_metadata(grade, subject)

    def get_recent_homework_summary(
        self, *, student_id: str | None = None, class_id: str | None = None
    ) -> dict[str, Any]:
        """获取近期作业摘要。"""
        return self.homework_skill.fetch_recent_homework_summary(
            student_id=student_id,
            class_id=class_id,
        )
