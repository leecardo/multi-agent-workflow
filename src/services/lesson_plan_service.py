"""教案模板服务。"""

from __future__ import annotations

from typing import Any

from src.repositories import PostgresRepository
from src.skills import ResourcePlatformSkill


class LessonPlanService:
    """提供教案模板与案例推荐。"""

    def __init__(
        self,
        repository: PostgresRepository | None = None,
        resource_skill: ResourcePlatformSkill | None = None,
    ) -> None:
        self.repository = repository or PostgresRepository()
        self.resource_skill = resource_skill or ResourcePlatformSkill()

    def get_template(self, scenario: str) -> dict[str, Any]:
        """获取模板。"""
        return self.repository.get_lesson_plan_template(scenario)

    def get_recommended_cases(
        self, *, grade: str, subject: str, topic: str
    ) -> list[dict[str, Any]]:
        """获取推荐案例。"""
        return self.resource_skill.fetch_recommended_resources(
            grade=grade,
            subject=subject,
            topic=topic,
        )
