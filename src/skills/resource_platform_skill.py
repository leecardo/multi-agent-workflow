"""校本资源平台能力封装。"""

from __future__ import annotations

from typing import Any


class ResourcePlatformSkill:
    """读取外部资源平台返回的推荐资源。"""

    def fetch_recommended_resources(
        self, *, grade: str, subject: str, topic: str
    ) -> list[dict[str, Any]]:
        """返回资源推荐结果。"""
        return [
            {
                "title": f"{grade}{subject}《{topic}》示范课例",
                "type": "lesson_case",
                "highlights": ["问题链设计", "易错点提醒"],
            },
            {
                "title": f"{topic}课堂活动单",
                "type": "activity_sheet",
                "highlights": ["小组讨论", "分层练习"],
            },
        ]
