"""学生画像服务。"""

from __future__ import annotations

from typing import Any

from src.repositories import PostgresRepository
from src.skills import HomeworkPlatformSkill, SchoolUserSkill


class StudentProfileService:
    """聚合学生画像、用户信息与近期作业表现。"""

    def __init__(
        self,
        repository: PostgresRepository | None = None,
        user_skill: SchoolUserSkill | None = None,
        homework_skill: HomeworkPlatformSkill | None = None,
    ) -> None:
        self.repository = repository or PostgresRepository()
        self.user_skill = user_skill or SchoolUserSkill()
        self.homework_skill = homework_skill or HomeworkPlatformSkill()

    def get_profile(self, student_id: str) -> dict[str, Any]:
        """获取学生画像。"""
        profile = self.repository.get_student_profile(student_id)
        user_summary = self.user_skill.fetch_user_summary(user_id=student_id)
        homework_summary = self.homework_skill.fetch_recent_homework_summary(student_id=student_id)
        return {
            **profile,
            "user_summary": user_summary,
            "homework_summary": homework_summary,
        }
