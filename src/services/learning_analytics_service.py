"""学情分析服务。"""

from __future__ import annotations

from typing import Any

from src.repositories import PostgresRepository
from src.skills import ExamSystemSkill, HomeworkPlatformSkill


class LearningAnalyticsService:
    """聚合结构化学情指标与外部系统摘要。"""

    def __init__(
        self,
        repository: PostgresRepository | None = None,
        exam_skill: ExamSystemSkill | None = None,
        homework_skill: HomeworkPlatformSkill | None = None,
    ) -> None:
        self.repository = repository or PostgresRepository()
        self.exam_skill = exam_skill or ExamSystemSkill()
        self.homework_skill = homework_skill or HomeworkPlatformSkill()

    def get_learning_overview(self, *, class_id: str, subject: str) -> dict[str, Any]:
        """获取学情概览。"""
        metrics = self.repository.get_learning_metrics(class_id)
        exam_summary = self.exam_skill.fetch_exam_summary(class_id=class_id, subject=subject)
        homework_summary = self.homework_skill.fetch_recent_homework_summary(class_id=class_id)
        return {
            "metrics": metrics,
            "exam_summary": exam_summary,
            "homework_summary": homework_summary,
        }
