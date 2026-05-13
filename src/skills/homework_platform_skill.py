"""作业平台能力封装。"""

from __future__ import annotations

from typing import Any


class HomeworkPlatformSkill:
    """访问作业平台的摘要信息。"""

    def fetch_recent_homework_summary(
        self, *, student_id: str | None = None, class_id: str | None = None
    ) -> dict[str, Any]:
        """返回最近作业摘要。"""
        return {
            "student_id": student_id,
            "class_id": class_id,
            "completion_rate": 0.9,
            "recent_focus": ["基础计算", "步骤规范"],
            "wrong_causes": ["审题不完整", "计算粗心"],
        }
