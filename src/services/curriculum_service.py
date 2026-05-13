"""课程标准服务。"""

from __future__ import annotations

from typing import Any

from src.repositories import PostgresRepository


class CurriculumService:
    """提供课程标准访问能力。"""

    def __init__(self, repository: PostgresRepository | None = None) -> None:
        self.repository = repository or PostgresRepository()

    def get_standard(self, grade: str, subject: str) -> dict[str, Any]:
        """获取课程标准摘要。"""
        return self.repository.get_curriculum_standard(grade, subject)
