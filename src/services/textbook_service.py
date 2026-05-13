"""教材服务。"""

from __future__ import annotations

from src.repositories import PostgresRepository


class TextbookService:
    """提供教材片段访问能力。"""

    def __init__(self, repository: PostgresRepository | None = None) -> None:
        self.repository = repository or PostgresRepository()

    def get_sections(self, grade: str, subject: str) -> list[dict[str, str]]:
        """获取教材章节摘要。"""
        return self.repository.get_textbook_sections(grade, subject)
