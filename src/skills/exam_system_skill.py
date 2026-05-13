"""考试系统能力封装。"""

from __future__ import annotations

from typing import Any


class ExamSystemSkill:
    """读取考试系统摘要。"""

    def fetch_exam_summary(self, *, class_id: str, subject: str | None = None) -> dict[str, Any]:
        """返回考试汇总。"""
        return {
            "class_id": class_id,
            "subject": subject or "相关学科",
            "exam_count": 3,
            "score_trend": [82, 79, 85],
            "weak_points": ["应用题建模", "表达规范"],
        }
